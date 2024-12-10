from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtGui import QPainter, QColor, QTextCharFormat, QSyntaxHighlighter
from PyQt5.QtCore import Qt, QRegExp

class YamlEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_editor()
        self.highlighter = YamlHighlighter(self.document())
        
    def setup_editor(self):
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #272822;
                color: #F8F8F2;
                font-family: 'Courier New';
                font-size: 12pt;
            }
        """)

class YamlHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlightingRules = []
        self.setup_highlighting_rules()
        
    def setup_highlighting_rules(self):
        # Define formats for different syntax elements
        key_format = QTextCharFormat()
        key_format.setForeground(QColor("#1E90FF"))
        
        # Add rules for YAML syntax
        keywords = ['id', 'info', 'name', 'author', 'severity', 'tags']
        for keyword in keywords:
            pattern = QRegExp(f"\\b{keyword}\\b(?=\\s*:)")
            self.highlightingRules.append((pattern, key_format))