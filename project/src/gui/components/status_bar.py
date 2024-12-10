
from PyQt5.QtWidgets import QStatusBar, QLabel
from PyQt5.QtCore import Qt

class StatusBar(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        # POC计数标签
        self.poc_count_label = QLabel()
        self.poc_count_label.setAlignment(Qt.AlignLeft)
        self.addWidget(self.poc_count_label, 1)
        
        # 状态信息标签
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignRight)
        self.addPermanentWidget(self.status_label)
        
    def update_poc_count(self, count):
        self.poc_count_label.setText(f'POC总数: {count}')
        
    def set_status(self, message):
        self.status_label.setText(message)
