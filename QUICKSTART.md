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
# Quick Start Guide for LLM Assistants

This guide is specifically for LLM assistants to help users set up the Code Signature Tool.

## Context

This tool helps freelancers automatically add their professional contact information to code files. It's designed to work transparently via Git hooks.

## Setup Process (For LLMs)

### Step 1: Understand User Requirements

Ask the user for their contact information:

```
I'll help you set up the code signature tool. I need the following information:

1. Your full name
2. Your professional title (e.g., "Software Engineer", "AI Engineer")
3. Your website (if you have one)
4. Your contact email
5. Your Upwork profile URL (if applicable)
```

### Step 2: Run Installation

```bash
cd code-signature-tool
./install.sh
```

The script will:
- Create `~/.signature.json` with user's information
- Install the tool to `~/bin/add-signatures`
- Set up global Git hooks
- Install VS Code snippets (optional)

### Step 3: Verify Installation

Test that everything works:

```bash
# Test 1: Config exists
cat ~/.signature.json

# Test 2: Tool is accessible
add-signatures --help

# Test 3: Process test files
cd examples/sample_files
add-signatures --dry-run

# Test 4: Actually add signatures
add-signatures
cat example.py  # Should show signature at top
```

### Step 4: Test Git Hook

```bash
# Create a test repository
mkdir test-repo
cd test-repo
git init

# Create a test file
echo 'print("hello")' > test.py

# Commit it
git add test.py
git commit -m "test"

# Check if signature was added
cat test.py
```

Expected output:
```python
# ================================================================================
# Author: [User's Name]
# Title: [User's Title]
# Website: [User's Website]
# Email: [User's Email]
# Upwork: [User's Upwork URL]
# Created: 2025-11-21
# ================================================================================
print("hello")
```

## Common Issues & Solutions

### Issue: "Python 3 required but not found"
**Solution:** Install Python 3:
```bash
# Ubuntu/Debian
sudo apt install python3

# macOS
brew install python3
```

### Issue: "~/bin not in PATH"
**Solution:** Add to shell config:
```bash
# For bash
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# For zsh
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Issue: Git hook not running
**Solution:** Verify hook setup:
```bash
# Check Git config
git config --global core.hooksPath
# Should output: /home/username/.git-hooks

# Check hook exists and is executable
ls -la ~/.git-hooks/pre-commit
# Should show: -rwxr-xr-x
```

### Issue: Signatures not added to certain file types
**Solution:** Check if file type is supported:
```bash
python3 -c "
from signature_tool.generator import get_supported_extensions
print('Supported extensions:')
for ext in get_supported_extensions():
    print(f'  {ext}')
"
```

## Testing Checklist

After installation, verify these items:

- [ ] Config file exists: `~/.signature.json`
- [ ] Tool is executable: `add-signatures --help` works
- [ ] Git hook installed: `~/.git-hooks/pre-commit` exists
- [ ] Git configured: `git config --global core.hooksPath` shows hooks path
- [ ] Manual command works: `add-signatures` adds signatures to files
- [ ] Git hook works: Signatures automatically added on commit
- [ ] Signature detection works: Running twice doesn't duplicate signatures
- [ ] VS Code snippets work: Type `sig` + Tab inserts signature

## Per-Project Customization

If user needs different contact info for a specific project:

```bash
cd /path/to/project

# Create local config (overrides global)
cat > .signature.json << EOF
{
  "email": "project-specific@email.com"
}
EOF

# Now commits in this project will use the project-specific email
```

## Updating Contact Information

If user wants to change their information:

```bash
# Edit global config
nano ~/.signature.json

# Update existing files with new info
cd /path/to/project
add-signatures --force

# Reinstall VS Code snippets with new info
cd /path/to/code-signature-tool
./install.sh
# Say "yes" when asked to install VS Code snippets
```

## Usage Patterns

### Pattern 1: New File (VS Code)
1. User creates new file in VS Code
2. Types `sig` then presses Tab
3. Signature inserted automatically

### Pattern 2: Existing Files (Git Hook)
1. User creates/edits files
2. Runs `git commit`
3. Pre-commit hook adds signatures automatically
4. Commit proceeds with signatures

### Pattern 3: Before Delivery (Manual)
1. User finishes project
2. Runs `add-signatures --dry-run` to preview
3. Runs `add-signatures` to add signatures to all files
4. Delivers project to client

## Troubleshooting Commands

```bash
# Check Python syntax
python3 -m py_compile src/signature_tool/*.py

# Test config loading
python3 -c "
import sys
sys.path.insert(0, 'src')
from signature_tool.config import load_config
config = load_config()
print(f'Author: {config[\"author\"]}')
"

# Test signature generation
python3 -c "
import sys
sys.path.insert(0, 'src')
from signature_tool.generator import generate_signature
config = {'author': 'Test', 'email': 'test@example.com'}
print(generate_signature(config, '.py'))
"

# Test file processing
python3 -c "
import sys
sys.path.insert(0, 'src')
from pathlib import Path
from signature_tool.config import load_config
from signature_tool.processor import process_files
config = load_config()
stats = process_files(config.to_dict(), Path('.'), dry_run=True)
print(f'Would process: {stats[\"processed\"]} files')
"
```

## Success Criteria

Installation is successful when:

1. ✅ User can run `add-signatures --help`
2. ✅ Sample files show signatures after running `add-signatures`
3. ✅ Git commits automatically add signatures to new files
4. ✅ VS Code snippet (`sig` + Tab) works
5. ✅ User understands how to use the tool

## Next Steps

After successful installation, remind the user:

1. **For new files:** Type `sig` + Tab in VS Code
2. **For existing projects:** Run `add-signatures` before delivery
3. **Automatic mode:** Just commit - signatures added automatically
4. **Update info:** Edit `~/.signature.json` anytime

## Support

If issues persist:
- Check `README.md` for detailed documentation
- Review `docs/DESIGN.md` for architecture details
- Test individual components using troubleshooting commands above
