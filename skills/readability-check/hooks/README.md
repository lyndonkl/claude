# Automatic readability checks via Claude Code hooks

Optional. The skill works without hooks; these make it run on its own so long prose gets checked whether or not anyone remembers to ask.

## Contents

- [What it does](#what-it-does)
- [Install](#install)
- [Configuration](#configuration)
- [Advisory vs blocking](#advisory-vs-blocking)
- [Safety properties](#safety-properties)
- [Troubleshooting](#troubleshooting)

## What it does

One script, `readability_hook.py`, handles two events and branches on `hook_event_name`:

| Event | Fires when | Checks |
|---|---|---|
| `Stop` | Claude finishes a turn | `last_assistant_message`, if it is long enough |
| `PostToolUse` | after `Write` or `Edit` | the file just written, if its extension matches |

Both are gated on a **300-word minimum**. Short replies and small files are skipped, because readability formulas are unstable on short text and the advice would be noise.

When prose fails, the hook returns the failing metrics plus the specific over-length sentences. Claude sees that on its next turn and can act on it.

## Install

### If you installed the plugin — already wired, still off

The plugin ships `hooks/hooks.json` at its root, so both hooks register automatically on install. They use `${CLAUDE_PLUGIN_ROOT}`, so the paths survive plugin updates.

**They do nothing until you opt in.** Installing a plugin should not silently change how your sessions behave. Two steps to turn it on:

```bash
python3 -m pip install --user textstat
```

Then set the flag in `~/.claude/settings.json`:

```json
{
  "env": {
    "READABILITY_HOOK_ENABLED": "1"
  }
}
```

That is the whole setup. To turn it off again, remove the variable.

### If you are not using the plugin

Add the hooks yourself, pointing at your clone. Replace `/ABSOLUTE/PATH/TO/claude` with the real path:

```json
{
  "env": {
    "READABILITY_HOOK_ENABLED": "1"
  },
  "hooks": {
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"/ABSOLUTE/PATH/TO/claude/skills/readability-check/hooks/readability_hook.py\"",
            "timeout": 15
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"/ABSOLUTE/PATH/TO/claude/skills/readability-check/hooks/readability_hook.py\"",
            "timeout": 15,
            "statusMessage": "Checking readability..."
          }
        ]
      }
    ]
  }
}
```

**Only want one of the two?** Keep just that block. Checking written documents is the higher-value half if you pick one.

### Verify

Test the script directly, without a session:

```bash
READABILITY_HOOK_ENABLED=1 python3 -c "
import json
print(json.dumps({
  'hook_event_name': 'Stop', 'session_id': 't', 'prompt_id': 't',
  'last_assistant_message': 'The service handles validation and dedup and enrichment ' * 40
}))" | READABILITY_HOOK_ENABLED=1 python3 readability_hook.py
```

Expect JSON with a report. Silence with exit 0 means the hook ran and had nothing to say — which is also what you get if the flag is unset, so check the flag first when debugging.

## Configuration

Set environment variables in the `env` block of `settings.json`, or export them before launching:

| Variable | Default | Effect |
|---|---|---|
| `READABILITY_HOOK_ENABLED` | *(off)* | **Master switch.** `1`, `true`, `yes`, or `on` to run at all |
| `READABILITY_HOOK_PROFILE` | `general` | `technical`, `general`, or `public` |
| `READABILITY_HOOK_MIN_WORDS` | `300` | Word floor below which nothing is checked |
| `READABILITY_HOOK_MODE` | `advisory` | `advisory` or `block` |
| `READABILITY_HOOK_EXTENSIONS` | `.md,.txt,.mdx` | Extensions checked by the `PostToolUse` half |

Example — check engineering docs against the technical profile, only for markdown:

```json
{
  "env": {
    "READABILITY_HOOK_PROFILE": "technical",
    "READABILITY_HOOK_EXTENSIONS": ".md"
  }
}
```

## Advisory vs blocking

**`advisory` (default)** — exits 0 and returns the report through `additionalContext`. Claude sees it next turn. Nothing is interrupted.

**`block`** — exits 2, which feeds the report to Claude and prevents the turn from completing until it responds. Stronger, and riskier: a `Stop` hook that blocks every failing draft can loop, because the rewrite may also fail.

The loop guard makes blocking safe: **the hook blocks at most once per turn.** It writes a marker keyed on `session_id` + `prompt_id` to the system temp directory, and any second failure in the same turn falls back to advisory. If the marker cannot be written, it treats that as "already blocked" and stays advisory — failing toward the safer behavior.

Start with `advisory`. Move to `block` only if advisory findings are being ignored.

## Safety properties

The hook is built to be boring in every failure case:

1. **Off until asked.** Registered on plugin install, inert until `READABILITY_HOOK_ENABLED` is set. The flag is checked before stdin is even read.
2. **Fails open.** Missing `textstat`, unreadable file, malformed payload, unexpected exception — every path exits 0 silently. A broken check is acceptable; a broken session is not.
3. **Never blocks more than once per turn**, even in blocking mode.
4. **Reads only.** It scores text and prints a report. It does not edit files.
5. **Skips short text**, so ordinary conversation is untouched.
6. **Bounded output.** At most three quoted sentences, each truncated at 200 characters.
7. **No network.** Everything runs locally.

## Troubleshooting

**Nothing happens.** Usually correct: the text was under 300 words, or it passed. Check with `--stdin` directly:

```bash
cat draft.md | python3 ../resources/readability.py --stdin --profile general
```

**Nothing happens even on long failing prose.** Confirm `textstat` is installed for the *same* interpreter the hook uses:

```bash
python3 -c "import textstat; print(textstat.__version__)"
```

If that fails, the hook is silently failing open by design. Install the package.

**Too noisy.** Raise `READABILITY_HOOK_MIN_WORDS`, or switch the profile to `technical`.

**Firing on files it should not.** Narrow `READABILITY_HOOK_EXTENSIONS`, or drop the `PostToolUse` block and keep only `Stop`.

**Want it off temporarily.** Unset `READABILITY_HOOK_ENABLED`. That is the master switch and it disables both hooks immediately.
