---
name: markdown-to-pdf
description: Renders a markdown report to a PDF using pandoc with xelatex (11pt serif body, 1-inch margins, numbered footnotes, formal heading hierarchy). Requires a one-time install of pandoc and a LaTeX engine on the user's machine — basictex on macOS or texlive-xetex on Linux. Does not attempt automatic install. Fails loudly with the exact install commands if pandoc or xelatex is missing on the user's PATH. Use when producing a finished strategist or analyst report PDF from a polished markdown source.
---

# Markdown-to-PDF rendering

Converts a finished markdown report to a PDF using pandoc and the xelatex engine, with formatting tuned for analyst-style output.

## One-time install (user-side)

This skill assumes pandoc and a LaTeX engine are already on the user's PATH. It does not install anything. If either tool is missing, the render command exits with the exact install instructions and the user installs once.

**macOS:**

```bash
brew install pandoc basictex
sudo tlmgr update --self
sudo tlmgr install xetex
```

`basictex` is about 90 MB. Do not install `mactex` unless the user specifically needs the full LaTeX stack (~5 GB).

**Linux (Debian/Ubuntu):**

```bash
sudo apt install pandoc texlive-xetex texlive-fonts-recommended
```

After installation, open a new shell so `xelatex` is on PATH.

## Workflow

Copy this checklist into the working response and tick each step as it completes:

```
Markdown-to-PDF render:
- [ ] Step 1: Verify the input markdown file exists.
- [ ] Step 2: Verify pandoc is on PATH. If missing, print the pandoc install block and stop.
- [ ] Step 3: Verify xelatex is on PATH. If missing, print the xelatex install block and stop.
- [ ] Step 4: Create the output directory if it does not already exist.
- [ ] Step 5: Run the pandoc command exactly as specified below.
- [ ] Step 6: Confirm the output PDF file exists. Report its path.
```

### Step 2 — verify pandoc

```bash
command -v pandoc
```

If this exits non-zero, print the block in "Failure messages" labelled *pandoc-missing* and stop. Do not proceed to Step 5.

### Step 3 — verify xelatex

```bash
command -v xelatex
```

If this exits non-zero, print the block in "Failure messages" labelled *xelatex-missing* and stop. Do not proceed to Step 5.

### Step 5 — exact pandoc invocation

Substitute the input and output paths but do not modify any flag:

```bash
pandoc <INPUT_MD> \
  --from markdown+footnotes+yaml_metadata_block \
  --pdf-engine=xelatex \
  --output <OUTPUT_PDF> \
  --variable geometry:margin=1in \
  --variable papersize=letter \
  --variable fontsize=11pt \
  --variable linestretch=1.2 \
  --variable colorlinks=true \
  --variable linkcolor=black \
  --variable urlcolor=black \
  --variable toccolor=black
```

The variables are tuned for analyst-style output: letter-size paper, 1-inch margins, 11pt body at 1.2 line height, all hyperlinks rendered in black so the printed page reads cleanly.

### Step 6 — verify the output

```bash
test -s <OUTPUT_PDF> && echo "PDF rendered: <OUTPUT_PDF>"
```

If the output file does not exist or is empty after pandoc returns success, treat that as a render failure and surface the pandoc stderr to the user.

## Failure messages

Print these blocks exactly as written. They are the contract with the user.

### pandoc-missing

```
ERROR: pandoc is not installed.

This skill requires pandoc and a LaTeX engine.

Install on macOS:
  brew install pandoc basictex
  sudo tlmgr update --self
  sudo tlmgr install xetex

Install on Linux (Debian/Ubuntu):
  sudo apt install pandoc texlive-xetex texlive-fonts-recommended

Open a new shell after installing so the new binaries are on PATH, then re-run.
```

### xelatex-missing

```
ERROR: xelatex is not installed.

pandoc is present, but the LaTeX engine (xelatex) is missing.

Install on macOS:
  brew install basictex
  sudo tlmgr update --self
  sudo tlmgr install xetex

Install on Linux (Debian/Ubuntu):
  sudo apt install texlive-xetex texlive-fonts-recommended

Open a new shell after installing, then re-run.
```

## Notes for the calling agent

- The markdown source should use pandoc-style numbered footnotes: `text.[^1]` in the body with `[^1]: ...` definitions later in the file. These render as proper LaTeX footnotes.
- If the markdown has a YAML front matter block with `title:`, `subtitle:`, and `date:` fields, those will appear in the rendered title block.
- Do not pre-process the markdown. The pandoc invocation above is the only transformation.
- Auto-install of pandoc or LaTeX is explicitly out of scope. The skill never modifies the user's machine.
- The skill never modifies the input markdown.
