from PyQt5.QtWidgets import (QWidget, QScrollArea, QGridLayout,
                             QPushButton, QLabel, QVBoxLayout)
from PyQt5.QtCore import Qt, pyqtSignal
from collections import Counter


class TagButton(QPushButton):
    def __init__(self, text, count, parent=None):
        super().__init__(parent)
        self.setText(f"{text} ({count})")
        self.setStyleSheet("""
            QPushButton {
                background-color: #e1e1e1;
                border: none;
                border-radius: 15px;
                padding: 5px 10px;
                margin: 2px;
                color: #333;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #d1d1d1;
            }
            QPushButton:pressed {
                background-color: #c1c1c1;
            }
        """)


class TagPanel(QScrollArea):
    tagSelected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWidgetResizable(True)
        self.setMaximumHeight(150)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 创建主容器
        container = QWidget()
        self.main_layout = QVBoxLayout(container)

        # 标题
        title = QLabel("热门标签 (点击筛选)")
        title.setStyleSheet("""
            QLabel {
                color: #333;
                font-weight: bold;
                padding: 5px;
                border-bottom: 1px solid #ddd;
            }
        """)
        self.main_layout.addWidget(title)

        # 标签网格容器
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(5)
        self.main_layout.addWidget(self.grid_widget)

        self.setWidget(container)

    def update_tags(self, yaml_data):
        """更新标签统计"""
        # 清除现有标签
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().setParent(None)

        # 统计标签
        all_tags = []
        for poc in yaml_data:
            info = poc.get('info', {})
            if isinstance(info, dict):
                tags = info.get('tags', [])
                if isinstance(tags, str):
                    tags = [tag.strip() for tag in tags.split(',')]
                elif isinstance(tags, list):
                    all_tags.extend(tag.strip() for tag in tags if tag)

        # 获取前100个最常用的标签
        tag_counter = Counter(all_tags)
        top_tags = tag_counter.most_common(100)

        # 创建标签按钮
        row = col = 0
        for tag, count in top_tags:
            btn = TagButton(tag, count)
            btn.clicked.connect(lambda checked, t=tag: self.tagSelected.emit(t))
            self.grid_layout.addWidget(btn, row, col)

            col += 1
            if col >= 10:  # 每行10个标签
                col = 0
                row += 1