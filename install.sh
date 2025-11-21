#!/usr/bin/env bash
# ==============================================================================
# Installation script for Code Signature Tool
#
# This script will:
# 1. Create global configuration at ~/.signature.json
# 2. Install the Python tool
# 3. Set up global Git hooks
# 4. Optionally install VS Code snippets
# ==============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Code Signature Tool - Installation${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Step 1: Check prerequisites
echo -e "${YELLOW}[1/5]${NC} Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not found${NC}"
    exit 1
fi

if ! command -v git &> /dev/null; then
    echo -e "${RED}Error: Git is required but not found${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Prerequisites OK"
echo ""

# Step 2: Create global configuration
echo -e "${YELLOW}[2/5]${NC} Setting up global configuration..."

CONFIG_FILE="$HOME/.signature.json"

if [ -f "$CONFIG_FILE" ]; then
    echo -e "${YELLOW}⚠${NC}  Configuration already exists at $CONFIG_FILE"
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}→${NC} Keeping existing configuration"
    else
        rm "$CONFIG_FILE"
    fi
fi

if [ ! -f "$CONFIG_FILE" ]; then
    # Prompt for user information
    echo "Please enter your contact information:"
    echo ""

    read -p "Full Name: " AUTHOR
    read -p "Professional Title: " TITLE
    read -p "Website: " WEBSITE
    read -p "Email: " EMAIL
    read -p "Upwork Profile URL (optional): " UPWORK

    # Create config file
    cat > "$CONFIG_FILE" << EOF
{
  "author": "$AUTHOR",
  "title": "$TITLE",
  "website": "$WEBSITE",
  "email": "$EMAIL"$([ -n "$UPWORK" ] && echo ",
  \"upwork\": \"$UPWORK\"" || echo "")
}
EOF

    echo -e "${GREEN}✓${NC} Configuration created at $CONFIG_FILE"
else
    echo -e "${GREEN}✓${NC} Using existing configuration"
fi
echo ""

# Step 3: Install Python tool
echo -e "${YELLOW}[3/5]${NC} Installing Python tool..."

# Option 1: Try to install as package (if setup.py exists)
if [ -f "$SCRIPT_DIR/setup.py" ] || [ -f "$SCRIPT_DIR/pyproject.toml" ]; then
    echo -e "${BLUE}→${NC} Installing via pip..."
    pip install -e "$SCRIPT_DIR" || {
        echo -e "${YELLOW}⚠${NC}  Package installation failed, falling back to manual installation"
    }
fi

# Option 2: Manual installation to ~/bin
mkdir -p "$HOME/bin"

# Create wrapper script
cat > "$HOME/bin/add-signatures" << 'WRAPPER_EOF'
#!/usr/bin/env python3
import sys
from pathlib import Path

# Add signature_tool to path
tool_path = Path(__file__).parent.parent / "code-signature-tool" / "src"
if tool_path.exists():
    sys.path.insert(0, str(tool_path))

from signature_tool.cli import main

if __name__ == '__main__':
    main()
WRAPPER_EOF

chmod +x "$HOME/bin/add-signatures"

echo -e "${GREEN}✓${NC} Tool installed to ~/bin/add-signatures"

# Check if ~/bin is in PATH
if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
    echo -e "${YELLOW}⚠${NC}  ~/bin is not in your PATH"
    echo -e "${BLUE}→${NC} Add this line to your ~/.bashrc or ~/.zshrc:"
    echo -e "    export PATH=\"\$HOME/bin:\$PATH\""
fi
echo ""

# Step 4: Set up global Git hooks
echo -e "${YELLOW}[4/5]${NC} Setting up Git hooks..."

HOOKS_DIR="$HOME/.git-hooks"
mkdir -p "$HOOKS_DIR"

# Copy pre-commit hook
cp "$SCRIPT_DIR/hooks/pre-commit" "$HOOKS_DIR/pre-commit"
chmod +x "$HOOKS_DIR/pre-commit"

# Configure Git to use global hooks
git config --global core.hooksPath "$HOOKS_DIR"

echo -e "${GREEN}✓${NC} Git hooks installed to $HOOKS_DIR"
echo -e "${GREEN}✓${NC} Git configured to use global hooks"
echo ""

# Step 5: VS Code snippets (optional)
echo -e "${YELLOW}[5/5]${NC} Installing VS Code snippets..."

read -p "Do you want to install VS Code snippets? (Y/n): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
    VSCODE_SNIPPETS_DIR=""

    # Detect VS Code snippets directory
    if [ -d "$HOME/.config/Code/User/snippets" ]; then
        VSCODE_SNIPPETS_DIR="$HOME/.config/Code/User/snippets"
    elif [ -d "$HOME/Library/Application Support/Code/User/snippets" ]; then
        VSCODE_SNIPPETS_DIR="$HOME/Library/Application Support/Code/User/snippets"
    elif [ -d "$APPDATA/Code/User/snippets" ]; then
        VSCODE_SNIPPETS_DIR="$APPDATA/Code/User/snippets"
    fi

    if [ -n "$VSCODE_SNIPPETS_DIR" ]; then
        # Update snippets with user's config
        for snippet_file in "$SCRIPT_DIR/.vscode/snippets"/*.json; do
            if [ -f "$snippet_file" ]; then
                # Replace placeholder values with actual config
                sed -e "s/Vivek Patel/$AUTHOR/g" \
                    -e "s|https://vivekapatel.com|$WEBSITE|g" \
                    -e "s|contact@vivekapatel.com|$EMAIL|g" \
                    -e "s|AI Engineer | Computer Vision Specialist|$TITLE|g" \
                    "$snippet_file" > "$VSCODE_SNIPPETS_DIR/$(basename "$snippet_file")"
            fi
        done
        echo -e "${GREEN}✓${NC} VS Code snippets installed to $VSCODE_SNIPPETS_DIR"
    else
        echo -e "${YELLOW}⚠${NC}  VS Code snippets directory not found"
        echo -e "${BLUE}→${NC} You can manually copy snippets from $SCRIPT_DIR/.vscode/snippets/"
    fi
else
    echo -e "${BLUE}→${NC} Skipping VS Code snippets"
fi
echo ""

# Done!
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Installation Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "What's next?"
echo ""
echo "1. Test the tool:"
echo -e "   ${BLUE}add-signatures --dry-run${NC}"
echo ""
echo "2. Create a test file and commit it:"
echo -e "   ${BLUE}echo 'print(\"hello\")' > test.py${NC}"
echo -e "   ${BLUE}git add test.py && git commit -m \"test\"${NC}"
echo -e "   ${BLUE}cat test.py  # Should have your signature${NC}"
echo ""
echo "3. Use VS Code snippets:"
echo -e "   ${BLUE}Type 'sig' then press Tab in any code file${NC}"
echo ""
echo "Configuration file: $CONFIG_FILE"
echo "To update your info, edit this file and reinstall snippets"
echo ""
