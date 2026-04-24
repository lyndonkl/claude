---
name: normalize-format
description: Normalizes a single inbox file of any supported format (plain markdown, Claude.ai JSON export, Claude Code JSONL session, Readwise markdown/CSV highlight, transcript with timestamps or speaker labels, link capture) into a clean markdown body plus partial frontmatter (id, title, source block, word_count). Handles format-specific failure modes — JSON content-block arrays, timestamp stripping, per-highlight chunking, URL-vs-commentary separation. Use when ingesting any inbox item for the substacker Librarian. Trigger keywords: normalize, convert, parse, transcript, export, JSON, JSONL, highlight, CSV.
---

# Normalize Format

## Table of Contents

- [Supported formats](#supported-formats)
- [Workflow](#workflow)
- [Detection heuristics](#detection-heuristics)
- [Worked example](#worked-example)
- [Guardrails](#guardrails)

**Related skills:** Called by `ingest-inbox-item` as step 1. Upstream of `tag-by-topic`, `score-intuition-density`, `dedupe-against-corpus`.

## Supported formats

| Extension | Format | Notes |
|---|---|---|
| `.md`, `.txt` | plain markdown | Default; passes through |
| `.json` | Claude.ai export | Conversation with messages array |
| `.jsonl` | Claude Code session | Content-block array per response |
| `.md` (Readwise-shaped) | Readwise export | Highlights + user notes |
| `.csv` | Readwise CSV | Per-row highlight |
| `.vtt`, `.srt`, `.md` (diarized) | Transcript | May include timestamps + speaker labels |
| `.md` with URL + commentary | Link capture | User's framing is the signal |

## Workflow

```
Normalize one file:
- [ ] Step 1: Detect format by extension + first-line sniff
- [ ] Step 2: Apply format-specific parse
- [ ] Step 3: Split long transcripts at topic boundaries (>3000 words)
- [ ] Step 4: Emit [{body, partial_frontmatter}, ...] list (usually one item)
```

### Step 1: Detection

- `.jsonl` with `"type":"assistant"` → Claude Code session.
- `.json` with `"conversation"` / `"messages"` top-level key → Claude.ai export.
- `.md` starting with `# ` and Readwise boilerplate (`**Highlights first synced by Readwise...**`) → Readwise.
- `.vtt` / `.srt`, or `.md` with `[HH:MM:SS]` timestamp pattern, or lines prefixed with speaker labels like `Me:` → transcript.
- `.md` with ≤50 words and a prominent URL → link capture.
- Else: plain markdown.

### Step 2: Format-specific parse

**Plain markdown**: pass body through unchanged. Title = first H1 or filename-derived.

**Claude.ai JSON**: flatten content blocks to markdown. Preserve user/assistant turn labels (`**Me:**` / `**Claude:**`). Strip system-reminder blocks. `provenance.author: claude`, `confidence: paraphrased`.

**Claude Code JSONL**: flatten content-block array. Drop `tool_use` blocks unless the adjacent user message references the tool output. Strip system reminders.

**Readwise**: split per-book file into one seed per highlight. Body = highlight + user note. Boilerplate stripped. For bare highlights (no user note), set `provenance.confidence: quoted`, density capped at 3 downstream. For user-annotated highlights, `confidence: owned`.

**Transcript**: strip timestamps. Preserve speaker labels as `**Speaker:**` prefixes. If >3000 words, split at topic shifts — emit multiple outputs sharing `parent_source`. Target ~1500 words per chunk.

**Link capture**: separate URL from commentary. Body = user's commentary. Frontmatter adds `source.linked_url`. If <50 words of commentary, flag `low_commentary: true` so the scorer caps density.

### Step 3: Split long transcripts

Split heuristic: paragraph break + topic-vocabulary shift (measured by tag overlap drop across adjacent paragraphs). Each chunk ~1500 words. Preserve `parent_source` across chunks.

## Detection heuristics

- A file that looks like a transcript but is actually an email thread (first-line sniff: `From: ...`, `Date: ...`, `Subject: ...`) — reclassify as plain markdown or link capture.
- A Readwise file missing boilerplate — treat as plain markdown.
- A `.json` file that isn't a Claude export — treat as plain markdown and wrap in code fences.

## Worked example

**Input** (`inbox/2026-04-21-claude-bnn.json`):
```json
{"conversation":{"name":"BNN variational","messages":[
  {"role":"user","content":[{"type":"text","text":"help me intuit why variational inference..."}]},
  {"role":"assistant","content":[{"type":"text","text":"Think of it as fitting a simple distribution..."}]}
]}}
```

**Output**:
```markdown
# BNN variational

**Me:** help me intuit why variational inference...

**Claude:** Think of it as fitting a simple distribution...
```

With `partial_frontmatter = {id: 2026-04-21-bnn-variational, title: "BNN variational", source: {type: claude-conversation, ...}, provenance: {author: claude, confidence: paraphrased}}`.

## Guardrails

1. Readwise CSV with malformed rows: skip the row, log `WARN | malformed CSV row in <file> line N` to changelog.
2. Claude.ai JSON schema drift: if `messages` key missing, fall back to recursive text extraction; mark `confidence: paraphrased` regardless.
3. Transcript that is actually an email thread: reclassify rather than keep as transcript.
4. Never OCR images. Image-only inbox items get a seed body of `[image: awaiting user annotation]` and `status: dead` with reason `image-only`.
5. Files >50k words: refuse and log. User splits manually.
6. Never lose the original. Even if parsing fails, the inbox file stays intact (caller moves to `.processed/` only on success).

## Quick reference

- Seven supported formats, each with a specific parser.
- Returns `[{body, partial_frontmatter}, ...]` — always a list, usually of length 1.
- Long transcripts split into multiple outputs sharing `parent_source`.
