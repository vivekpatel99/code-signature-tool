# Code Signature Tool

Automatically add your professional signature to all code and documentation files. Perfect for freelancers who want to maintain attribution in delivered projects.

## What This Does

- **Automatically adds your contact info** to the top of every code file you create
- **Works with Git hooks** - signatures added automatically when you commit
- **VS Code snippets** - type `sig` + Tab to insert signature in new files
- **Global configuration** - set up once, works in all projects
- **Local overrides** - customize per-project if needed

## Generated Signature Example

```python
# ==============================================================================
# Author: Vivek Patel
# Title: AI Engineer | Computer Vision Specialist
# Website: https://vivekapatel.com
# Email: contact@vivekapatel.com
# Upwork: https://www.upwork.com/freelancers/vivekpatel99?mp_source=share
# Created: 2025-11-21
# ==============================================================================
```

## Quick Start (For LLMs)

**To set up this tool for a user, run these commands in order:**

```bash
# 1. Clone or use this repository
cd code-signature-tool

# 2. Run the installation script
chmod +x install.sh
./install.sh

# 3. Edit ~/.signature.json with user's information
# (Script will prompt for this)
```

## Installation (Detailed)

### Prerequisites

- Python 3.8+
- Git
- VS Code (optional, for snippets)

### Automatic Installation

```bash
./install.sh
```

This will:
1. Create global config at `~/.signature.json`
2. Install the signature tool
3. Set up global Git hooks
4. Configure VS Code snippets (if requested)

### Manual Installation

If you prefer manual setup:

#### 1. Create Global Configuration

```bash
cat > ~/.signature.json << 'EOF'
{
  "author": "Your Name",
  "title": "Your Title/Role",
  "website": "https://yourwebsite.com",
  "email": "your@email.com",
  "upwork": "https://www.upwork.com/freelancers/~yourprofile"
}
EOF
```

#### 2. Install Python Tool

```bash
# Option A: Install as package
pip install -e .

# Option B: Copy to ~/bin
mkdir -p ~/bin
cp src/signature_tool/cli.py ~/bin/add-signatures
chmod +x ~/bin/add-signatures
```

#### 3. Set Up Global Git Hooks

```bash
# Create hooks directory
mkdir -p ~/.git-hooks

# Copy pre-commit hook
cp hooks/pre-commit ~/.git-hooks/pre-commit
chmod +x ~/.git-hooks/pre-commit

# Configure Git to use global hooks
git config --global core.hooksPath ~/.git-hooks
```

#### 4. Add VS Code Snippets (Optional)

Copy snippet files to VS Code:

```bash
# Linux/Mac
cp .vscode/snippets/* ~/.config/Code/User/snippets/

# Windows
# cp .vscode/snippets/* %APPDATA%/Code/User/snippets/
```

## Usage

### Automatic (Recommended)

Once installed, signatures are added automatically when you commit:

```bash
git add myfile.py
git commit -m "Add feature"
# Signature automatically added to myfile.py before commit completes
```

### Manual Script

Add signatures to all files in current project:

```bash
add-signatures
```

**Options:**
- `--dry-run` - Show what would change without modifying files
- `--force` - Update existing signatures
- `--path <dir>` - Process specific directory

### VS Code Snippets

In any supported file:
1. Type `sig`
2. Press Tab
3. Signature inserted at cursor

## Adding Signatures to Existing Projects

### Single Project

Navigate to your project and run:

```bash
cd /path/to/your/project

# Preview what will change
~/bin/add-signatures --dry-run

# Add signatures to all files
~/bin/add-signatures
```

### Multiple Projects in One Directory

Update all projects in a parent directory:

```bash
cd ~/projects

# Preview changes for all projects
for dir in */; do
    echo "=== $dir ==="
    cd "$dir"
    ~/bin/add-signatures --dry-run | grep "Processed:"
    cd ..
done

# Apply signatures to all projects
for dir in */; do
    echo "Processing $dir..."
    cd "$dir"
    ~/bin/add-signatures
    cd ..
done
```

### Specific Project Path (Copy-Paste Ready)

Replace `/path/to/project` with your actual path:

```bash
# Single project
cd /path/to/project && ~/bin/add-signatures

# Preview first
cd /path/to/project && ~/bin/add-signatures --dry-run
```

**Example paths:**
```bash
# Example 1: Upwork project
cd ~/freelance/01_active/upwork/ProjectName/03_development && ~/bin/add-signatures

# Example 2: Portfolio project
cd ~/freelance/portfolio/my-project && ~/bin/add-signatures

# Example 3: Client project
cd ~/projects/client-name/project-folder && ~/bin/add-signatures
```

### Update and Commit

Add signatures and commit them:

```bash
cd /path/to/project
~/bin/add-signatures
git add -u  # Add only modified files
git commit -m "Add professional signatures to code files"
```

### What Gets Processed

The tool automatically **processes:**
- ✅ Python files (`.py`)
- ✅ JavaScript/TypeScript (`.js`, `.ts`, `.jsx`, `.tsx`)
- ✅ Markdown documentation (`.md`)
- ✅ Other code files (see Supported File Types below)

The tool automatically **skips:**
- ✅ `.venv/`, `node_modules/`, `__pycache__/` (dependencies)
- ✅ `.git/`, `.idea/`, `.vscode/` (IDE/VCS folders)
- ✅ `.claude/` directory (Claude Code config)
- ✅ Hidden files (`.env`, `.gitignore`, etc.)
- ✅ Lock files (`package-lock.json`, `poetry.lock`, etc.)
- ✅ Files in your ignore list (see Configuration below)

## Configuration

### Global Config

`~/.signature.json` - Used for all projects

```json
{
  "author": "Your Name",
  "title": "Your Professional Title",
  "website": "https://yourwebsite.com",
  "email": "your@email.com",
  "upwork": "https://www.upwork.com/freelancers/~yourprofile"
}
```

### Local Override (Optional)

`.signature.json` in project root - Overrides global config for this project

```json
{
  "email": "project-specific@email.com"
}
```

Local config merges with global - only override fields you need to change.

### Ignore List (Optional)

Add an `"ignore"` field to exclude specific files or patterns:

```json
{
  "author": "Your Name",
  "email": "your@email.com",
  "ignore": [
    "CLAUDE.md",
    "**/CLAUDE.md",
    ".claude/*",
    ".claude/**",
    ".*",
    "package-lock.json",
    "requirements.txt",
    "LICENSE",
    "CHANGELOG*"
  ]
}
```

**Common ignore patterns:**

| Pattern | What It Ignores |
|---------|----------------|
| `"CLAUDE.md"` | File named CLAUDE.md |
| `"**/CLAUDE.md"` | CLAUDE.md in any directory |
| `".*"` | Hidden files (`.env`, `.gitignore`) |
| `".claude/**"` | Entire .claude directory |
| `"*.log"` | All log files |
| `"test_*.py"` | Test files starting with test_ |
| `"**/node_modules/**"` | Node modules (already skipped by default) |

**Already skipped by default:**
- `.venv/`, `node_modules/`, `__pycache__/`
- `.git/`, `.idea/`, `.vscode/`
- `.gitignore`, `LICENSE`, `requirements.txt`
- `package-lock.json`, `yarn.lock`, `poetry.lock`

## Supported File Types

| Language | Extension | Comment Style |
|----------|-----------|---------------|
| Python | `.py` | `#` |
| JavaScript | `.js` | `//` |
| TypeScript | `.ts`, `.tsx` | `//` |
| React | `.jsx` | `//` |
| Markdown | `.md` | `<!-- -->` |
| HTML | `.html` | `<!-- -->` |
| CSS | `.css`, `.scss` | `/* */` |
| Shell | `.sh`, `.bash` | `#` |
| Go | `.go` | `//` |
| Rust | `.rs` | `//` |
| Java | `.java` | `//` |
| C/C++ | `.c`, `.cpp`, `.h` | `//` |

## How It Works

### Git Hook Flow

```
You: git commit -m "message"
  ↓
Pre-commit hook runs
  ↓
Scans staged files
  ↓
Adds signatures to files without them
  ↓
Re-stages modified files
  ↓
Commit proceeds with signatures
```

### Signature Detection

The tool checks if a file already has a signature by:
1. Reading first 20 lines
2. Looking for your email address
3. If found, skips the file (unless `--force` flag)

### Date Handling

- **New signatures:** Uses current date (YYYY-MM-DD)
- **Existing signatures:** Preserves original creation date

## Troubleshooting

### Hook Not Running

```bash
# Check Git hooks path
git config --global core.hooksPath

# Should output: /home/username/.git-hooks

# Verify hook is executable
ls -la ~/.git-hooks/pre-commit
# Should show: -rwxr-xr-x
```

### Config Not Found

```bash
# Check if config exists
cat ~/.signature.json

# If missing, create it
./install.sh
```

### Signature Not Added to File

```bash
# Check if file type is supported
add-signatures --dry-run

# Run with verbose output (if implemented)
add-signatures --verbose

# Manually test
python -m signature_tool.cli --path .
```

## Uninstallation

```bash
# Remove global Git hooks
git config --global --unset core.hooksPath

# Remove config
rm ~/.signature.json

# Remove tool (if installed via pip)
pip uninstall signature-tool

# Remove VS Code snippets
rm ~/.config/Code/User/snippets/python.json
rm ~/.config/Code/User/snippets/javascript.json
# ... etc
```

## Development

### Project Structure

```
code-signature-tool/
├── src/
│   └── signature_tool/
│       ├── __init__.py
│       ├── config.py          # Config loading & merging
│       ├── generator.py       # Signature generation
│       ├── processor.py       # File processing
│       └── cli.py            # Command-line interface
├── hooks/
│   └── pre-commit            # Git hook script
├── .vscode/
│   └── snippets/             # VS Code snippet templates
│       ├── python.json
│       ├── javascript.json
│       ├── typescript.json
│       └── markdown.json
├── examples/
│   ├── .signature.json       # Example local config
│   └── sample_files/         # Test files
├── docs/
│   └── DESIGN.md            # Full design documentation
├── tests/                    # Unit tests
├── install.sh               # Installation script
├── pyproject.toml           # Python package config
└── README.md               # This file
```

### Running Tests

```bash
# Run unit tests
pytest tests/

# Test on sample files
add-signatures --path examples/sample_files --dry-run
```

## For LLM Assistants

When setting up this tool for a user:

1. **Ask for their contact information:**
   - Full name
   - Professional title
   - Website
   - Email
   - Upwork profile URL (if applicable)

2. **Run installation:**
   ```bash
   cd code-signature-tool
   ./install.sh
   ```

3. **Edit `~/.signature.json`** with their information

4. **Test the setup:**
   ```bash
   # Create test file
   echo "print('hello')" > test.py

   # Run signature tool
   add-signatures --path . --dry-run

   # Verify it would add signature
   add-signatures --path .

   # Check result
   cat test.py
   ```

5. **Verify Git hook:**
   ```bash
   git init test-repo
   cd test-repo
   echo "console.log('test')" > test.js
   git add test.js
   git commit -m "test"
   cat test.js  # Should have signature
   ```

6. **Confirm with user** that signature looks correct

## License

MIT License - Feel free to modify and distribute

## Contributing

PRs welcome! Please ensure:
- Code passes tests
- New file types include comment style mapping
- Documentation updated

## Author

Created by Vivek Patel for freelance project attribution

## Support

Issues: https://github.com/yourusername/code-signature-tool/issues
