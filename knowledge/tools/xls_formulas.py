#!/usr/bin/env python3
"""Extract formulas from BIFF8 .xls files by decoding FORMULA record rgce."""
import sys, struct
import xlrd
from xlrd.compdoc import CompDoc

FUNCS = {1:'IF',4:'SUM',5:'AVERAGE',6:'MIN',7:'MAX',15:'SIN',20:'SQRT',21:'EXP',22:'LN',23:'LOG10',24:'ABS',
         25:'INT',26:'SIGN',27:'ROUND',28:'LOOKUP',29:'INDEX',36:'AND',37:'OR',38:'NOT',39:'MOD',
         64:'MATCH',102:'VLOOKUP',101:'HLOOKUP',109:'LOG',337:'POWER',345:'SUMIF',346:'COUNTIF'}

def colname(c):
    s=''
    c0=c
    while True:
        s=chr(ord('A')+c0%26)+s
        c0=c0//26-1
        if c0<0: break
    return s

def ref(row,colflags):
    col=colflags&0x3FFF
    rel_c=colflags&0x4000; rel_r=colflags&0x8000
    return ('' if rel_c else '$')+colname(col)+('' if rel_r else '$')+str(row+1)

def decode(rgce, sheetnames, externsheet):
    i=0; stack=[]
    n=len(rgce)
    ops={0x03:'+',0x04:'-',0x05:'*',0x06:'/',0x07:'^',0x08:'&',0x09:'<',0x0A:'<=',0x0B:'=',0x0C:'>=',0x0D:'>',0x0E:'<>'}
    try:
        while i<n:
            ptg=rgce[i]; i+=1
            if 0x40<=ptg<0x60: base=ptg-0x20
            elif 0x60<=ptg<0x80: base=ptg-0x40
            else: base=ptg
            if ptg in ops:
                b=stack.pop(); a=stack.pop(); stack.append(f'({a}{ops[ptg]}{b})')
            elif ptg==0x12: pass  # uplus
            elif ptg==0x13: stack.append('-'+stack.pop())
            elif ptg==0x14: stack.append(stack.pop()+'%')
            elif ptg==0x15: stack.append('('+stack.pop()+')')
            elif ptg==0x16: stack.append('')  # missing arg
            elif ptg==0x01:
                r,c=struct.unpack('<HH',rgce[i:i+4]); i+=4
                stack.append(f'<SHARED@{colname(c)}{r+1}>')
            elif ptg==0x17:
                ln=rgce[i]; opt=rgce[i+1]; i+=2
                if opt&1:
                    s=rgce[i:i+ln*2].decode('utf-16le'); i+=ln*2
                else:
                    s=rgce[i:i+ln].decode('latin1'); i+=ln
                stack.append('"'+s+'"')
            elif ptg==0x19:
                sub=rgce[i]; i+=3  # attr: skip (space/sum/if/choose jumps)
                if sub&0x04:  # choose: extra jump table
                    cnt=struct.unpack('<H',rgce[i-2:i])[0]
                    i+=2*(cnt+1)
                if sub&0x10 and stack:  # attrSum
                    stack.append('SUM('+stack.pop()+')')
            elif ptg==0x1C: stack.append('#ERR'); i+=1
            elif ptg==0x1D: stack.append(str(bool(rgce[i]))); i+=1
            elif ptg==0x1E:
                stack.append(str(struct.unpack('<H',rgce[i:i+2])[0])); i+=2
            elif ptg==0x1F:
                v=struct.unpack('<d',rgce[i:i+8])[0]; i+=8
                stack.append(repr(v))
            elif base==0x21 or base==0x22:
                if base==0x22:
                    argc=rgce[i]; iftab=struct.unpack('<H',rgce[i+1:i+3])[0]; i+=3
                else:
                    iftab=struct.unpack('<H',rgce[i:i+2])[0]; i+=2
                    argc={1:2,4:1,22:1,21:1,20:1,24:1,102:3}.get(iftab,1)
                fn=FUNCS.get(iftab,f'FUNC{iftab}')
                args=[stack.pop() for _ in range(argc)][::-1]
                stack.append(fn+'('+','.join(args)+')')
            elif base==0x24:
                r,cf=struct.unpack('<HH',rgce[i:i+4]); i+=4
                stack.append(ref(r,cf))
            elif base==0x25:
                r1,r2,c1,c2=struct.unpack('<HHHH',rgce[i:i+8]); i+=8
                stack.append(ref(r1,c1)+':'+ref(r2,c2))
            elif base==0x3A:
                ixti,r,cf=struct.unpack('<HHH',rgce[i:i+6]); i+=6
                sh=externsheet.get(ixti,('?','?'))
                stack.append(f"'{sh}'!"+ref(r,cf))
            elif base==0x3B:
                ixti,r1,r2,c1,c2=struct.unpack('<HHHHH',rgce[i:i+10]); i+=10
                sh=externsheet.get(ixti,('?','?'))
                stack.append(f"'{sh}'!"+ref(r1,c1)+':'+ref(r2,c2))
            elif ptg==0x2C or ptg==0x4C or ptg==0x6C:  # RefN
                r,cf=struct.unpack('<HH',rgce[i:i+4]); i+=4
                stack.append(f'RefN({r},{cf})')
            else:
                return f'<undecoded ptg 0x{ptg:02X} at {i-1}; raw={rgce.hex()}>'
        return stack[-1] if stack else '<empty>'
    except Exception as e:
        return f'<decode error {e}; raw={rgce.hex()}>'

def main(path):
    with open(path,'rb') as f: data=f.read()
    cd=CompDoc(data)
    mem=off=length=None
    for nm in (u'Workbook', u'Book'):
        try:
            mem,off,length=cd.locate_named_stream(nm)
        except Exception:
            mem=None
        if mem is not None: break
    stream=bytes(mem[off:off+length])
    book=xlrd.open_workbook(path)
    sheetnames=book.sheet_names()
    # parse BOUNDSHEET records for order (globals substream first)
    pos=0; nrec=0
    sheet_idx=-1
    externsheet={}
    supbook_sheets=sheetnames
    results={}
    while pos+4<=len(stream):
        opcode,ln=struct.unpack('<HH',stream[pos:pos+4])
        payload=stream[pos+4:pos+4+ln]
        if opcode==0x0809:  # BOF
            dt=struct.unpack('<H',payload[2:4])[0]
            if dt==0x0010:
                sheet_idx+=1
        elif opcode==0x0017:  # EXTERNSHEET
            cnt=struct.unpack('<H',payload[0:2])[0]
            for k in range(cnt):
                sb,f1,l1=struct.unpack('<HHH',payload[2+6*k:8+6*k])
                nm=sheetnames[f1] if 0<=f1<len(sheetnames) else f'sheet{f1}'
                if f1!=l1: nm+=':'+ (sheetnames[l1] if 0<=l1<len(sheetnames) else f'sheet{l1}')
                externsheet[k]=nm
        elif opcode==0x0006 and sheet_idx>=0:  # FORMULA
            row,col=struct.unpack('<HH',payload[0:4])
            cce=struct.unpack('<H',payload[20:22])[0]
            rgce=payload[22:22+cce]
            frm=decode(rgce,sheetnames,externsheet)
            results.setdefault(sheet_idx,[]).append((row,col,frm))
        pos+=4+ln
    for si in sorted(results):
        print(f'--- SHEET {sheetnames[si] if si<len(sheetnames) else si} ---')
        for row,col,frm in results[si]:
            print(f'{colname(col)}{row+1}: ={frm}')

if __name__=='__main__':
    main(sys.argv[1])
