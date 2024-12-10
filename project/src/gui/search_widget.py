from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt


class SearchWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()

        # 搜索说明
        help_label = QLabel("支持 && 和 || 运算符，例如: 'sql && rce' 或 'sql || xss'")
        help_label.setStyleSheet("""
            QLabel {
                color: #666;
                font-size: 12px;
                padding: 5px;
            }
        """)
        layout.addWidget(help_label)

        # 搜索输入框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("全局搜索")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
                min-width: 300px;
            }
        """)
        layout.addWidget(self.search_input)

        # 搜索按钮
        self.search_button = QPushButton('搜索')
        self.search_button.setStyleSheet("""
            QPushButton {
                padding: 5px 15px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        layout.addWidget(self.search_button)

        # 重置按钮
        self.reset_button = QPushButton('重置')
        self.reset_button.setStyleSheet("""
            QPushButton {
                padding: 5px 15px;
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        layout.addWidget(self.reset_button)

        self.setLayout(layout)

    def set_parent(self, parent):
        """设置父组件以便调用搜索方法"""
        self.parent = parent
        self.search_input.returnPressed.connect(self.on_search_clicked)
        self.search_button.clicked.connect(self.on_search_clicked)
        self.reset_button.clicked.connect(self.on_reset_clicked)

    def on_search_clicked(self):
        """执行搜索"""
        if hasattr(self, 'parent'):
            keyword = self.search_input.text().strip()
            self.parent.search_table(keyword)

    def on_reset_clicked(self):
        """重置搜索"""
        self.search_input.clear()
        if hasattr(self, 'parent'):
            self.parent.reset_search()