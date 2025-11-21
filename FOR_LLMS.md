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
# Instructions for LLM Assistants

## Purpose

This repository contains a complete, production-ready tool for automatically adding professional signatures to code files. It's designed for freelance developers who want to maintain attribution in their delivered projects.

## When to Use This

A user might ask:
- "I want to add my contact info to all my code files"
- "How can I automatically sign my code for client projects?"
- "I need attribution in files I deliver to clients"
- "Can you help me set up code signatures?"

## Quick Setup (3 Commands)

```bash
cd code-signature-tool
./install.sh
# Follow prompts to enter user's contact information
```

That's it! The tool is now installed and will work automatically.

## What Gets Installed

1. **Global config** at `~/.signature.json` with user's contact info
2. **Python tool** at `~/bin/add-signatures` for manual usage
3. **Git hook** at `~/.git-hooks/pre-commit` for automatic insertion
4. **VS Code snippets** for manual insertion via `sig` + Tab

## How It Works

### Automatic Mode (Default)
User creates/edits files → commits with Git → signatures automatically added

### Manual Mode
User runs `add-signatures` command → signatures added to all files

### Snippet Mode
User types `sig` then Tab in VS Code → signature inserted at cursor

## Generated Signature Example

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

## Testing After Installation

```bash
# Test 1: Verify config
cat ~/.signature.json

# Test 2: Process example files
cd examples/sample_files
add-signatures
cat example.py  # Should show signature

# Test 3: Git hook
cd /tmp
mkdir test-repo && cd test-repo
git init
echo 'print("hello")' > test.py
git add test.py
git commit -m "test"
cat test.py  # Should show signature
```

## Supported File Types

Python, JavaScript, TypeScript, React (JSX/TSX), Markdown, HTML, CSS/SCSS, Shell, Ruby, Go, Rust, Java, C/C++, Swift, Kotlin, PHP, YAML, and more.

See `src/signature_tool/generator.py` for complete list.

## Configuration

### Global (All Projects)
Edit `~/.signature.json` to update contact information globally

### Per-Project Override
Create `.signature.json` in project root to override specific fields:
```json
{
  "email": "project-specific@email.com"
}
```

## Common User Questions

**Q: Will this work for all my projects?**
A: Yes, once installed globally, it works for every Git repository on the machine.

**Q: Can I customize signatures per project?**
A: Yes, create a local `.signature.json` file to override global settings.

**Q: What if I don't want signatures in a specific project?**
A: Delete the `.git/hooks/pre-commit` link in that project, or use `git commit --no-verify`.

**Q: Can I update my contact info later?**
A: Yes, edit `~/.signature.json` and run `add-signatures --force` to update existing files.

**Q: Will this slow down my commits?**
A: No, the hook only processes staged files and runs in milliseconds.

## Troubleshooting

### Problem: Hook not running
```bash
git config --global core.hooksPath
# Should show: /home/username/.git-hooks

# If not set:
git config --global core.hooksPath ~/.git-hooks
```

### Problem: Tool not found
```bash
# Check if ~/bin is in PATH
echo $PATH | grep "$HOME/bin"

# If not, add to ~/.bashrc or ~/.zshrc:
export PATH="$HOME/bin:$PATH"
```

### Problem: Wrong comment syntax
The tool auto-detects file type by extension. If a file has the wrong syntax, it might be unsupported. Check `src/signature_tool/generator.py` for supported types.

## Files Overview

| File | Purpose |
|------|---------|
| `README.md` | User-facing documentation |
| `QUICKSTART.md` | Step-by-step setup guide for LLMs |
| `FOR_LLMS.md` | This file - quick reference |
| `docs/DESIGN.md` | Complete technical design |
| `install.sh` | One-command installation script |
| `src/signature_tool/` | Python package with all logic |
| `hooks/pre-commit` | Git hook for automatic insertion |
| `.vscode/snippets/` | VS Code snippet templates |
| `examples/` | Sample files and config |

## Key Design Decisions

1. **Non-blocking** - Git hook never prevents commits (graceful degradation)
2. **Idempotent** - Running multiple times won't duplicate signatures
3. **Flexible** - Global config + per-project overrides
4. **Safe** - Respects .gitignore, skips binary files, handles errors gracefully
5. **LLM-friendly** - Clear docs, simple setup, easy to test

## Advanced Usage

### Dry Run (Preview Changes)
```bash
add-signatures --dry-run
```

### Force Update Existing Signatures
```bash
add-signatures --force
```

### Process Specific Directory
```bash
add-signatures --path ./src
```

### Verbose Output
```bash
add-signatures --verbose
```

## Publishing to GitHub

After customizing for the user:

```bash
# Update remote (replace with user's GitHub URL)
git remote add origin https://github.com/username/code-signature-tool.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Integration with Other Tools

- Works with any Git client (command line, VS Code, GitHub Desktop)
- Compatible with CI/CD pipelines
- No conflicts with other Git hooks (can be combined)
- Language-agnostic (works with any text file type)

## Success Criteria

Installation is successful when:
1. ✅ `add-signatures --help` works
2. ✅ Git commits automatically add signatures
3. ✅ VS Code snippet (`sig` + Tab) inserts signature
4. ✅ Existing signatures are detected (no duplicates)
5. ✅ User understands the three usage modes

## Future Enhancements

Ideas for future versions:
- Multiple signature templates
- License header integration
- Team mode (multiple authors)
- CI/CD validation
- IDE plugins for JetBrains, etc.

## Notes for LLMs

- This tool is **complete and tested** - no additional development needed
- Installation is **one command** - don't overcomplicate it
- **Test after installation** - verify it works before marking complete
- **Focus on user's contact info** - that's the only customization needed
- **Explain the three modes** - automatic, manual, snippet
- **Repository is ready to push** - just update the remote URL

## Support

For issues or questions:
- Check `README.md` for detailed user guide
- Review `QUICKSTART.md` for step-by-step setup
- Read `docs/DESIGN.md` for technical details
- Test individual components using code examples in `QUICKSTART.md`
