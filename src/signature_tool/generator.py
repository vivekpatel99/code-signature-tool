"""
Signature generator for different file types.

Generates properly formatted signatures with appropriate comment syntax.
"""

from datetime import datetime
from typing import Dict, Optional


# File extension to comment style mapping
COMMENT_STYLES = {
    # Hash comments
    '.py': 'hash',
    '.rb': 'hash',
    '.sh': 'hash',
    '.bash': 'hash',
    '.yaml': 'hash',
    '.yml': 'hash',
    '.r': 'hash',
    '.perl': 'hash',
    '.pl': 'hash',

    # Double-slash comments
    '.js': 'slash',
    '.ts': 'slash',
    '.jsx': 'slash',
    '.tsx': 'slash',
    '.java': 'slash',
    '.cpp': 'slash',
    '.c': 'slash',
    '.h': 'slash',
    '.hpp': 'slash',
    '.go': 'slash',
    '.rs': 'slash',
    '.swift': 'slash',
    '.kt': 'slash',
    '.scala': 'slash',
    '.php': 'slash',

    # HTML-style comments
    '.html': 'html',
    '.xml': 'html',
    '.md': 'html',
    '.svg': 'html',

    # CSS-style comments
    '.css': 'css',
    '.scss': 'css',
    '.sass': 'css',
    '.less': 'css',
}


class SignatureGenerator:
    """Generates formatted signatures for different file types."""

    def __init__(self, config: Dict, width: int = 80):
        """
        Initialize signature generator.

        Args:
            config: Configuration dictionary with author info
            width: Maximum width of signature block (default: 80)
        """
        self.config = config
        self.width = width
        self.separator = "=" * width

    def generate(self, file_extension: str, creation_date: Optional[str] = None) -> str:
        """
        Generate signature for given file type.

        Args:
            file_extension: File extension (e.g., '.py', '.js')
            creation_date: Creation date (YYYY-MM-DD), uses today if None

        Returns:
            Formatted signature string with appropriate comment syntax

        Raises:
            ValueError: If file extension is not supported
        """
        if file_extension not in COMMENT_STYLES:
            raise ValueError(f"Unsupported file extension: {file_extension}")

        comment_style = COMMENT_STYLES[file_extension]
        date = creation_date or datetime.now().strftime("%Y-%m-%d")

        # Build signature lines
        lines = [
            f"Author: {self.config['author']}",
        ]

        if 'title' in self.config:
            lines.append(f"Title: {self.config['title']}")

        if 'website' in self.config:
            lines.append(f"Website: {self.config['website']}")

        lines.append(f"Email: {self.config['email']}")

        if 'upwork' in self.config:
            lines.append(f"Upwork: {self.config['upwork']}")

        lines.append(f"Created: {date}")

        # Format with appropriate comment syntax
        return self._format_signature(lines, comment_style)

    def _format_signature(self, lines: list, style: str) -> str:
        """Format signature lines with appropriate comment syntax."""
        if style == 'hash':
            return self._format_hash(lines)
        elif style == 'slash':
            return self._format_slash(lines)
        elif style == 'html':
            return self._format_html(lines)
        elif style == 'css':
            return self._format_css(lines)
        else:
            raise ValueError(f"Unknown comment style: {style}")

    def _format_hash(self, lines: list) -> str:
        """Format with hash comments (#)."""
        result = [f"# {self.separator}"]
        for line in lines:
            result.append(f"# {line}")
        result.append(f"# {self.separator}")
        result.append("")  # Empty line after signature
        return "\n".join(result)

    def _format_slash(self, lines: list) -> str:
        """Format with double-slash comments (//)."""
        result = [f"// {self.separator}"]
        for line in lines:
            result.append(f"// {line}")
        result.append(f"// {self.separator}")
        result.append("")  # Empty line after signature
        return "\n".join(result)

    def _format_html(self, lines: list) -> str:
        """Format with HTML-style comments (<!-- -->)."""
        result = ["<!--"]
        result.append(self.separator)
        for line in lines:
            result.append(line)
        result.append(self.separator)
        result.append("-->")
        result.append("")  # Empty line after signature
        return "\n".join(result)

    def _format_css(self, lines: list) -> str:
        """Format with CSS-style comments (/* */)."""
        result = ["/*"]
        result.append(self.separator)
        for line in lines:
            result.append(line)
        result.append(self.separator)
        result.append("*/")
        result.append("")  # Empty line after signature
        return "\n".join(result)


def generate_signature(config: Dict, file_extension: str, creation_date: Optional[str] = None) -> str:
    """
    Generate signature for a file.

    Args:
        config: Configuration dictionary
        file_extension: File extension (e.g., '.py')
        creation_date: Optional creation date (YYYY-MM-DD)

    Returns:
        Formatted signature string
    """
    generator = SignatureGenerator(config)
    return generator.generate(file_extension, creation_date)


def is_supported_file(file_extension: str) -> bool:
    """Check if file extension is supported."""
    return file_extension in COMMENT_STYLES


def get_supported_extensions() -> list:
    """Get list of all supported file extensions."""
    return list(COMMENT_STYLES.keys())
