<!--
================================================================================
Author: Vivek Patel
Title: AI Engineer | Computer Vision Specialist
Website: https://vivekapatel.com
Email: contact@vivekapatel.com
Upwork: https://www.upwork.com/freelancers/vivekpatel99?mp_source=share
Created: 2025-11-21
================================================================================
-->
# Code Signature Tool - Design Documentation

**Date:** 2025-11-21
**Author:** Vivek Patel
**Version:** 1.0

---

## Overview

A comprehensive solution for automatically adding professional signatures to code files created by freelance developers. The tool ensures proper attribution and contact information is embedded in all project deliverables.

### Goals

1. **Automatic attribution** - Every file contains creator's contact information
2. **Zero-friction workflow** - Works transparently via Git hooks
3. **Global configuration** - Set up once, works everywhere
4. **Project flexibility** - Optional per-project overrides
5. **Multi-language support** - Proper comment syntax for each file type

### Non-Goals

- Tracking file modification history (use Git for this)
- Digital signatures or cryptographic verification
- License management or copyright enforcement
- Code analysis or quality checking

---

## System Architecture

### Components

```
┌─────────────────────────────────────────────────────────────┐
│                    User Workflow                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Create/Edit File                                        │
│     ├─ VS Code Snippet (type 'sig' + Tab)                  │
│     └─ Manual creation                                      │
│                                                              │
│  2. Git Commit                                              │
│     └─ Pre-commit Hook (automatic)                         │
│                                                              │
│  3. Manual Command (before delivery)                        │
│     └─ add-signatures --dry-run                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                 Configuration Layer                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Global Config: ~/.signature.json                           │
│  ├─ Author, Email, Website, Upwork, Title                  │
│  └─ Used across all projects                               │
│                                                              │
│  Local Config: ./.signature.json (optional)                │
│  ├─ Overrides global settings                              │
│  └─ Merged with global config                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                  Processing Engine                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Config Loader (config.py)                                  │
│  ├─ Load ~/.signature.json                                 │
│  ├─ Load ./.signature.json (if exists)                     │
│  ├─ Merge configs (local overrides global)                 │
│  └─ Validate required fields                               │
│                                                              │
│  Signature Generator (generator.py)                         │
│  ├─ Map file extension → comment style                     │
│  ├─ Format signature with proper syntax                    │
│  └─ Return formatted signature block                       │
│                                                              │
│  File Processor (processor.py)                              │
│  ├─ Check if signature exists (email in first 20 lines)   │
│  ├─ Handle shebang lines (#!)                             │
│  ├─ Insert signature at top of file                        │
│  └─ Skip binary files, respect .gitignore                  │
│                                                              │
│  CLI Interface (cli.py)                                     │
│  └─ Command-line flags, error handling, reporting          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Configuration System

### Global Configuration

**Location:** `~/.signature.json`

```json
{
  "author": "Vivek Patel",
  "title": "AI Engineer | Computer Vision Specialist",
  "website": "https://vivekapatel.com",
  "email": "contact@vivekapatel.com",
  "upwork": "https://www.upwork.com/freelancers/vivekpatel99"
}
```

**Required fields:** `author`, `email`
**Optional fields:** `title`, `website`, `upwork`

### Local Configuration Override

**Location:** `./.signature.json` (project root)

```json
{
  "email": "project-specific@email.com"
}
```

**Behavior:**
- Merges with global config
- Local values override global values
- Missing local fields use global defaults

**Use cases:**
- Project-specific email address
- Different professional title for specific client
- Omit certain contact info for particular projects

---

## Signature Generation

### Comment Style Mapping

| Extension | Language | Comment Style | Prefix | Suffix |
|-----------|----------|---------------|--------|--------|
| `.py` | Python | Hash | `#` | - |
| `.js`, `.ts` | JavaScript/TypeScript | Double-slash | `//` | - |
| `.md`, `.html` | Markdown/HTML | HTML comment | `<!--` | `-->` |
| `.css`, `.scss` | CSS | CSS comment | `/*` | `*/` |
| `.sh`, `.bash` | Shell | Hash | `#` | - |
| `.rb` | Ruby | Hash | `#` | - |
| `.go`, `.rs` | Go/Rust | Double-slash | `//` | - |
| `.java`, `.cpp` | Java/C++ | Double-slash | `//` | - |

### Signature Format

**Structure:**
1. Opening separator (80 equals signs)
2. Author information (one field per line)
3. Creation date (YYYY-MM-DD format)
4. Closing separator (80 equals signs)
5. Empty line

**Example (Python):**
```python
# ==============================================================================
# Author: Vivek Patel
# Title: AI Engineer | Computer Vision Specialist
# Website: https://vivekapatel.com
# Email: contact@vivekapatel.com
# Upwork: https://www.upwork.com/freelancers/vivekpatel99
# Created: 2025-11-21
# ==============================================================================

```

**Example (JavaScript):**
```javascript
// ==============================================================================
// Author: Vivek Patel
// Title: AI Engineer | Computer Vision Specialist
// Website: https://vivekapatel.com
// Email: contact@vivekapatel.com
// Upwork: https://www.upwork.com/freelancers/vivekpatel99
// Created: 2025-11-21
// ==============================================================================

```

**Example (Markdown):**
```markdown
<!--
==============================================================================
Author: Vivek Patel
Title: AI Engineer | Computer Vision Specialist
Website: https://vivekapatel.com
Email: contact@vivekapatel.com
Upwork: https://www.upwork.com/freelancers/vivekpatel99
Created: 2025-11-21
==============================================================================
-->

```

---

## File Processing Logic

### Signature Detection

**Algorithm:**
1. Read first 20 lines of file
2. Search for user's email address in any line
3. If found → signature exists
4. If not found → signature missing

**Why email?** Most unique identifier, unlikely to appear in regular code.

### Insertion Logic

**Normal files:**
```
[Signature Block]
[Empty Line]
[Original File Content]
```

**Files with shebang:**
```
#!/usr/bin/env python

[Signature Block]
[Empty Line]
[Rest of Original Content]
```

### Skip Conditions

Files are skipped if:
- Binary file (detected by encoding errors)
- Already has signature (unless `--force` flag)
- Unsupported file extension
- In ignored directories (`node_modules/`, `.venv/`, etc.)
- Specific files (`.gitignore`, `package-lock.json`, etc.)
- No read/write permissions

### Force Update

When `--force` flag is used:
1. Detect old signature block (by email presence)
2. Find end of signature (separator line or closing comment)
3. Remove old signature
4. Insert new signature
5. Preserve creation date if possible

---

## Git Hook Integration

### Pre-commit Hook Flow

```
User runs: git commit -m "message"
         ↓
Pre-commit hook triggers
         ↓
Get staged files: git diff --cached --name-only --diff-filter=ACM
         ↓
Filter for supported file types
         ↓
For each file:
  ├─ Check if signature exists
  ├─ Add signature if missing
  └─ Re-stage file: git add <file>
         ↓
Commit proceeds with signatures
```

### Hook Behavior

**Success cases:**
- Signatures added → Files re-staged → Commit proceeds
- All files have signatures → No action → Commit proceeds
- No staged files → Exit cleanly

**Failure cases (non-blocking):**
- Config missing → Warning message → Commit proceeds
- Tool not installed → Warning message → Commit proceeds
- Processing error → Error message → Commit proceeds

**Design principle:** Never block commits. If something fails, warn the user but allow the commit.

---

## VS Code Snippets

### Snippet Mechanism

**Trigger:** Type `sig` then press Tab
**Action:** Insert signature at cursor position
**Date:** Automatically uses current date via VS Code variables

### Snippet Variables

- `$CURRENT_YEAR` → 2025
- `$CURRENT_MONTH` → 11
- `$CURRENT_DATE` → 21
- `$0` → Final cursor position (after signature)

### Installation

**Global snippets:** `~/.config/Code/User/snippets/`
- Applied to all projects
- Easier to maintain
- Single source of truth

**Project snippets:** `.vscode/snippets/`
- Project-specific customization
- Can be committed to repo
- Useful for team standardization

---

## Installation & Setup

### Installation Script Flow

```bash
./install.sh
```

**Steps:**
1. ✓ Check prerequisites (Python 3, Git)
2. ✓ Create `~/.signature.json` (prompt for info)
3. ✓ Install Python tool to `~/bin/add-signatures`
4. ✓ Set up global Git hooks in `~/.git-hooks/`
5. ✓ Configure Git: `core.hooksPath = ~/.git-hooks`
6. ✓ Install VS Code snippets (optional)

### Manual Installation

For users who prefer manual setup or need to customize:

1. **Config:** Create `~/.signature.json` with contact info
2. **Tool:** Copy to `~/bin/` and add to PATH
3. **Hooks:** Copy to `~/.git-hooks/` and configure Git
4. **Snippets:** Copy to VS Code user snippets directory

---

## Command-Line Interface

### Usage

```bash
add-signatures [OPTIONS]
```

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `--path <dir>` | Process specific directory | Current directory |
| `--dry-run` | Show changes without modifying | False |
| `--force` | Update existing signatures | False |
| `--verbose` | Show detailed output | False |

### Examples

```bash
# Process current directory
add-signatures

# See what would change
add-signatures --dry-run

# Process specific directory
add-signatures --path ./src

# Update all existing signatures
add-signatures --force

# Verbose output
add-signatures --verbose --dry-run
```

### Output Format

```
Processing /path/to/project...

Results:
  Processed: 15 files
  Skipped:   42 files

Modified files:
  - src/main.py
  - src/utils.js
  - README.md
```

---

## Error Handling

### Configuration Errors

**Missing global config:**
```
Configuration error: Global configuration not found at ~/.signature.json

To create a configuration file, run:
  ./install.sh

Or manually create ~/.signature.json with:
  {"author": "Your Name", "email": "your@email.com"}
```

**Invalid JSON:**
```
Configuration error: Invalid JSON in ~/.signature.json:
  Expecting ',' delimiter: line 5 column 3
```

**Missing required fields:**
```
Configuration error: Missing required fields in configuration: author, email
Please update ~/.signature.json
```

### File Processing Errors

**Non-blocking errors:**
- Binary file → Skip silently
- Unsupported extension → Skip silently
- Permission denied → Warning, continue

**Blocking errors:**
- Path not found → Exit with error
- Config invalid → Exit with error

### Git Hook Errors

**All errors are non-blocking** to prevent commit interruption:
- Config missing → Warning + allow commit
- Tool not found → Warning + allow commit
- Processing error → Error message + allow commit

---

## Testing Strategy

### Unit Tests

**Config tests:**
- Load global config
- Load local config
- Merge configs correctly
- Validate required fields
- Handle invalid JSON

**Generator tests:**
- All comment styles render correctly
- Date formatting
- Optional fields handled
- Unsupported extensions raise error

**Processor tests:**
- Signature detection works
- Insertion at correct position
- Shebang handling
- Force update removes old signature
- Skip conditions work correctly

### Integration Tests

**End-to-end scenarios:**
1. Fresh install → configure → process files
2. Git commit → hook adds signatures → files staged
3. Local config override → signatures use local data
4. VS Code snippet → correct format inserted

### Manual Testing Checklist

- [ ] Install script completes successfully
- [ ] Config created at `~/.signature.json`
- [ ] Tool accessible via `add-signatures` command
- [ ] Git hook runs on commit
- [ ] Signatures added to new files automatically
- [ ] Signatures use correct comment syntax
- [ ] VS Code snippets work (type `sig` + Tab)
- [ ] Local config overrides global config
- [ ] Dry-run shows changes without modifying
- [ ] Force flag updates existing signatures

---

## Security & Privacy

### Sensitive Information

**User responsibilities:**
- Don't include sensitive data in config
- Review auto-generated signatures
- Consider privacy before sharing phone numbers

**Tool behavior:**
- Only reads user-controlled config files
- Never connects to network
- No telemetry or tracking
- All processing is local

### File Safety

**Protections:**
- Respects `.gitignore` patterns
- Skips system directories
- No recursive symlink following
- Validates file paths
- Handles permission errors gracefully

---

## Future Enhancements

### Potential Features

1. **Template system** - Multiple signature templates
2. **Project detection** - Auto-detect project name from Git
3. **License integration** - Add license headers
4. **Team mode** - Multiple authors in one project
5. **CI/CD integration** - Validate signatures in pipelines
6. **IDE plugins** - Native integration with JetBrains, etc.

### Extensibility Points

- Custom comment style handlers
- Additional file type support
- Hook system for signature customization
- Plugin architecture for new features

---

## Appendix

### Supported File Extensions

**Current (v1.0):**
`.py`, `.js`, `.ts`, `.jsx`, `.tsx`, `.md`, `.html`, `.css`, `.scss`, `.sh`, `.bash`, `.rb`, `.go`, `.rs`, `.java`, `.cpp`, `.c`, `.h`, `.hpp`, `.kt`, `.swift`, `.php`, `.yaml`, `.yml`, `.r`, `.pl`, `.scala`, `.sass`, `.less`, `.svg`, `.xml`

**Adding new types:**
1. Add extension to `COMMENT_STYLES` dict in `generator.py`
2. Map to appropriate comment style
3. Update documentation

### Directory Structure

```
code-signature-tool/
├── src/
│   └── signature_tool/
│       ├── __init__.py          # Package initialization
│       ├── config.py             # Configuration loader
│       ├── generator.py          # Signature generation
│       ├── processor.py          # File processing
│       └── cli.py               # CLI interface
├── hooks/
│   └── pre-commit               # Git pre-commit hook
├── .vscode/
│   └── snippets/                # VS Code snippet templates
│       ├── python.json
│       ├── javascript.json
│       ├── typescript.json
│       └── markdown.json
├── examples/
│   ├── .signature.json          # Example local config
│   └── sample_files/            # Test files
├── docs/
│   └── DESIGN.md               # This file
├── tests/                       # Unit tests
├── install.sh                   # Installation script
├── pyproject.toml               # Python package config
└── README.md                   # User documentation
```

### References

- [Git Hooks Documentation](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)
- [VS Code Snippets Guide](https://code.visualstudio.com/docs/editor/userdefinedsnippets)
- [Python Packaging Guide](https://packaging.python.org/en/latest/)

---

**Document Status:** Complete
**Last Updated:** 2025-11-21
**Next Review:** After user feedback from initial deployment
