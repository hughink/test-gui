from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt

class TableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()
        
    def initUI(self):
        self.setRowCount(23)
        self.setColumnCount(8)
        self.setHorizontalHeaderLabels([
            '序号', '文件名', '危害', '作者', 'tags', 'CVE编号', '参考链接', '漏洞描述'
        ])
        self.setup_table_style()
        
    def setup_table_style(self):
        self.setStyleSheet("""
            QTableWidget {
                background-color: #F3F3F3;
                alternate-background-color: #E8E8E8;
                color: #2D2D2D;
            }
            QTableWidget::item {
                border-bottom: 1px solid #D7D7D7;
            }
            QTableWidget::item:selected {
                background-color: #F0A30A;
                color: #FFFFFF;
            }
            QHeaderView::section {
                background-color: #9E9E9E;
                color: #2F2F2F;
                padding-left: 4px;
                border: 1px solid #BFBFBF;
                height: 25px;
            }
        """)