#!/usr/bin/env python3
"""
Detect clutter words and weak constructions in text.

Usage:
    python detect-clutter.py input.txt
    python detect-clutter.py input.txt --verbose
"""

import sys
import re
from pathlib import Path

# Clutter word lists
ADVERB_PATTERN = r'\b\w+ly\b'
QUALIFIERS = ['very', 'really', 'quite', 'rather', 'somewhat', 'fairly',
              'pretty', 'just', 'actually', 'basically', 'essentially',
              'totally', 'literally', 'absolutely', 'completely']
PASSIVE_PATTERNS = [
    (r'\bis\s+being\s+\w+ed\b', 'is being [verb]ed'),
    (r'\bare\s+being\s+\w+ed\b', 'are being [verb]ed'),
    (r'\bwas\s+\w+ed\b', 'was [verb]ed'),
    (r'\bwere\s+\w+ed\b', 'were [verb]ed'),
    (r'\bbeen\s+\w+ed\b', 'been [verb]ed'),
    (r'\bwas\s+being\s+\w+ed\b', 'was being [verb]ed'),
]
WEAK_VERBS = ['is', 'are', 'was', 'were', 'been', 'being', 'be', 'am']
WEAK_PHRASES = [
    'there is', 'there are', 'there was', 'there were',
    'it is', 'it was', 'it has been',
    'in order to', 'due to the fact that', 'at this point in time',
    'has the ability to', 'is able to', 'in the event that'
]

def detect_adverbs(text, line_num):
    """Detect adverbs (-ly words)."""
    findings = []
    for match in re.finditer(ADVERB_PATTERN, text, re.IGNORECASE):
        word = match.group()
        # Skip common words that aren't adverbs
        if word.lower() not in ['only', 'early', 'daily', 'weekly', 'monthly', 'yearly',
                                'likely', 'friendly', 'family', 'July', 'apply', 'supply']:
            findings.append({
                'line': line_num,
                'word': word,
                'context': get_context(text, match.start(), match.end()),
                'type': 'adverb'
            })
    return findings

def detect_qualifiers(text, line_num):
    """Detect qualifier words."""
    findings = []
    for qualifier in QUALIFIERS:
        pattern = r'\b' + re.escape(qualifier) + r'\b'
        for match in re.finditer(pattern, text, re.IGNORECASE):
            findings.append({
                'line': line_num,
                'word': match.group(),
                'context': get_context(text, match.start(), match.end()),
                'type': 'qualifier'
            })
    return findings

def detect_passive_voice(text, line_num):
    """Detect passive voice constructions."""
    findings = []
    for pattern, description in PASSIVE_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            findings.append({
                'line': line_num,
                'word': match.group(),
                'context': get_context(text, match.start(), match.end()),
                'type': 'passive',
                'description': description
            })
    return findings

def detect_weak_verbs(text, line_num):
    """Detect weak 'to be' verbs."""
    findings = []
    for verb in WEAK_VERBS:
        pattern = r'\b' + re.escape(verb) + r'\b'
        for match in re.finditer(pattern, text, re.IGNORECASE):
            # Get surrounding context to check if it's really weak
            context = get_context(text, match.start(), match.end(), window=20)
            # Skip if it's part of passive voice (already caught)
            if not re.search(r'\b\w+ed\b', context):
                findings.append({
                    'line': line_num,
                    'word': match.group(),
                    'context': context,
                    'type': 'weak_verb'
                })
    return findings

def detect_weak_phrases(text, line_num):
    """Detect weak phrases."""
    findings = []
    for phrase in WEAK_PHRASES:
        pattern = r'\b' + re.escape(phrase) + r'\b'
        for match in re.finditer(pattern, text, re.IGNORECASE):
            findings.append({
                'line': line_num,
                'word': match.group(),
                'context': get_context(text, match.start(), match.end()),
                'type': 'weak_phrase'
            })
    return findings

def get_context(text, start, end, window=40):
    """Get surrounding context for a match."""
    context_start = max(0, start - window)
    context_end = min(len(text), end + window)
    context = text[context_start:context_end]

    # Highlight the match
    match_start = start - context_start
    match_end = end - context_start
    highlighted = (context[:match_start] +
                  '[' + context[match_start:match_end] + ']' +
                  context[match_end:])

    return highlighted.replace('\n', ' ').strip()

def format_findings(findings_by_type, verbose=False):
    """Format findings into a report."""
    report = []
    report.append("Clutter Detection Report")
    report.append("=" * 50)
    report.append("")

    total_count = 0

    # Adverbs
    adverbs = findings_by_type.get('adverb', [])
    if adverbs:
        report.append(f"ADVERBS (-ly words): {len(adverbs)} found")
        for i, finding in enumerate(adverbs[:10 if not verbose else len(adverbs)], 1):
            report.append(f"Line {finding['line']}: \"{finding['context']}\"")
            report.append(f"  → Consider: Remove '{finding['word']}' or find stronger word")
        if len(adverbs) > 10 and not verbose:
            report.append(f"  ... and {len(adverbs) - 10} more (use --verbose to see all)")
        report.append("")
        total_count += len(adverbs)

    # Qualifiers
    qualifiers = findings_by_type.get('qualifier', [])
    if qualifiers:
        report.append(f"QUALIFIERS: {len(qualifiers)} found")
        for i, finding in enumerate(qualifiers[:10 if not verbose else len(qualifiers)], 1):
            report.append(f"Line {finding['line']}: \"{finding['context']}\"")
            report.append(f"  → Consider: Remove '{finding['word']}'")
        if len(qualifiers) > 10 and not verbose:
            report.append(f"  ... and {len(qualifiers) - 10} more (use --verbose to see all)")
        report.append("")
        total_count += len(qualifiers)

    # Passive voice
    passive = findings_by_type.get('passive', [])
    if passive:
        report.append(f"PASSIVE VOICE: {len(passive)} found")
        for i, finding in enumerate(passive[:10 if not verbose else len(passive)], 1):
            report.append(f"Line {finding['line']}: \"{finding['context']}\"")
            report.append(f"  → Consider: Convert to active voice")
        if len(passive) > 10 and not verbose:
            report.append(f"  ... and {len(passive) - 10} more (use --verbose to see all)")
        report.append("")
        total_count += len(passive)

    # Weak phrases
    weak_phrases = findings_by_type.get('weak_phrase', [])
    if weak_phrases:
        report.append(f"WEAK PHRASES: {len(weak_phrases)} found")
        for i, finding in enumerate(weak_phrases[:10 if not verbose else len(weak_phrases)], 1):
            report.append(f"Line {finding['line']}: \"{finding['context']}\"")
            report.append(f"  → Consider: Rewrite more directly")
        if len(weak_phrases) > 10 and not verbose:
            report.append(f"  ... and {len(weak_phrases) - 10} more (use --verbose to see all)")
        report.append("")
        total_count += len(weak_phrases)

    # Summary
    report.append("SUMMARY:")
    report.append(f"Total potential clutter: {total_count} instances")

    if total_count == 0:
        report.append("✓ No major clutter detected - well done!")
    elif total_count < 10:
        report.append("Severity: Low")
        report.append("Recommended action: Clean up flagged items")
    elif total_count < 30:
        report.append("Severity: Moderate")
        report.append("Recommended focus: Start with adverbs and qualifiers")
    else:
        report.append("Severity: High")
        report.append("Recommended action: Systematic clutter removal pass needed")

    if adverbs and len(adverbs) > total_count * 0.4:
        report.append("Primary issue: Adverbs (-ly words)")
    elif qualifiers and len(qualifiers) > total_count * 0.4:
        report.append("Primary issue: Qualifiers (very, really, quite, etc.)")

    return '\n'.join(report)

def main():
    """Main function."""
    verbose = '--verbose' in sys.argv

    # Read input from file or stdin
    if len(sys.argv) > 1 and sys.argv[1] != '--verbose':
        file_path = Path(sys.argv[1])
        if not file_path.exists():
            print(f"Error: File '{file_path}' not found", file=sys.stderr)
            sys.exit(1)
        try:
            text = file_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Read from stdin
        text = sys.stdin.read()

    if not text.strip():
        print("Error: No text to analyze", file=sys.stderr)
        sys.exit(1)

    # Analyze line by line
    findings_by_type = {
        'adverb': [],
        'qualifier': [],
        'passive': [],
        'weak_verb': [],
        'weak_phrase': []
    }

    lines = text.split('\n')
    for line_num, line in enumerate(lines, 1):
        if line.strip():
            findings_by_type['adverb'].extend(detect_adverbs(line, line_num))
            findings_by_type['qualifier'].extend(detect_qualifiers(line, line_num))
            findings_by_type['passive'].extend(detect_passive_voice(line, line_num))
            # findings_by_type['weak_verb'].extend(detect_weak_verbs(line, line_num))  # Too noisy
            findings_by_type['weak_phrase'].extend(detect_weak_phrases(line, line_num))

    # Generate and print report
    report = format_findings(findings_by_type, verbose)
    print(report)

if __name__ == '__main__':
    main()
