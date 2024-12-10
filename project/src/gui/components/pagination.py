
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import pyqtSignal

class Pagination(QWidget):
    pageChanged = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_page = 1
        self.total_pages = 1
        self.initUI()
        
    def initUI(self):
        layout = QHBoxLayout()
        
        # 上一页按钮
        self.prev_button = QPushButton('上一页')
        self.prev_button.clicked.connect(self.prev_page)
        
        # 页码显示
        self.page_label = QLabel()
        
        # 下一页按钮
        self.next_button = QPushButton('下一页')
        self.next_button.clicked.connect(self.next_page)
        
        # 跳转输入框
        self.goto_input = QLineEdit()
        self.goto_input.setFixedWidth(40)
        self.goto_input.setPlaceholderText('页码')
        
        # 跳转按钮
        self.goto_button = QPushButton('跳转')
        self.goto_button.clicked.connect(self.goto_page)
        
        # 添加组件到布局
        layout.addWidget(self.prev_button)
        layout.addWidget(self.page_label)
        layout.addWidget(self.next_button)
        layout.addWidget(self.goto_input)
        layout.addWidget(self.goto_button)
        
        self.setLayout(layout)
        self.update_page_label()
        
    def update_page_label(self):
        self.page_label.setText(f'第 {self.current_page} 页 / 共 {self.total_pages} 页')
        
    def set_total_pages(self, total):
        self.total_pages = max(1, total)
        self.update_page_label()
        
    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.pageChanged.emit(self.current_page)
            self.update_page_label()
            
    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.pageChanged.emit(self.current_page)
            self.update_page_label()
            
    def goto_page(self):
        try:
            page = int(self.goto_input.text())
            if 1 <= page <= self.total_pages:
                self.current_page = page
                self.pageChanged.emit(self.current_page)
                self.update_page_label()
                self.goto_input.clear()
        except ValueError:
            pass
