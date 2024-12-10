from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt

class SearchWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()
        
    def initUI(self):
        layout = QHBoxLayout()
        
        # 搜索说明
        help_label = QLabel("支持 && 和 || 运算符，例如: 'sql && rce' 或 'sql || xss'")
        help_label.setStyleSheet("color: #666;")
        layout.addWidget(help_label)
        
        # 搜索输入框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("全局搜索")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.textChanged.connect(self.on_search_text_changed)
        layout.addWidget(self.search_input)
        
        # 搜索按钮
        self.search_button = QPushButton('搜索')
        self.search_button.clicked.connect(self.on_search_clicked)
        layout.addWidget(self.search_button)
        
        # 重置按钮
        self.reset_button = QPushButton('重置')
        self.reset_button.clicked.connect(self.on_reset_clicked)
        layout.addWidget(self.reset_button)
        
        self.setLayout(layout)
        
    def on_search_text_changed(self, text):
        if not text:
            self.on_reset_clicked()
            
    def on_search_clicked(self):
        if hasattr(self.parent, 'search_table'):
            self.parent.search_table(self.search_input.text())
            
    def on_reset_clicked(self):
        self.search_input.clear()
        if hasattr(self.parent, 'reset_search'):
            self.parent.reset_search()

    def set_parent(self, self1):
        pass