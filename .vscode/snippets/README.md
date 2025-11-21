# VS Code Snippets

These snippet files allow you to quickly insert your signature by typing `sig` and pressing Tab.

## Installation

### Option 1: Global Snippets (Recommended)

Copy these files to your VS Code user snippets directory:

**Linux/Mac:**
```bash
cp *.json ~/.config/Code/User/snippets/
```

**Windows:**
```powershell
Copy-Item *.json $env:APPDATA\Code\User\snippets\
```

### Option 2: Manual Installation

1. Open VS Code
2. Go to: `File` → `Preferences` → `Configure User Snippets`
3. Select the language (e.g., "python")
4. Copy the content from the corresponding `.json` file
5. Paste it into the snippets file
6. Save

## Usage

1. Create a new file or open an existing one
2. Type `sig` at the location where you want the signature
3. Press `Tab`
4. The signature will be inserted with the current date

## Customization

To update your contact information in the snippets:

1. Edit each `.json` file
2. Replace the placeholder values with your information
3. Reinstall the snippets (if using global installation)

Or use the installation script which will automatically update these files with your config from `~/.signature.json`.

## Supported Languages

- `python.json` - Python files (`.py`)
- `javascript.json` - JavaScript files (`.js`)
- `typescript.json` - TypeScript files (`.ts`, `.tsx`)
- `markdown.json` - Markdown files (`.md`)

Add more snippet files for other languages as needed, following the same pattern.
