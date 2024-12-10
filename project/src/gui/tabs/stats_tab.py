import subprocess
import sys

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QLabel, QCheckBox, QPushButton,
                             QFrame, QScrollArea, QGridLayout, QMenu, QMessageBox,
                             QFileDialog, QApplication)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QCursor
from collections import Counter
import os
from ..components.search_widget import SearchWidget
from ..components.pagination import Pagination


class StatsTab(QWidget):
    pocSelected = pyqtSignal(str)  # Signal to notify when a POC is selected for editing

    def __init__(self, yaml_data):
        super().__init__()
        self.yaml_data = yaml_data or []
        self.filtered_yaml_data = []
        self.selected_pocs = set()
        self.rows_per_page = 50
        self.current_page = 1
        self.initUI()

    def calculate_statistics(self):
        stats = {
            'total': len(self.yaml_data),
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0,
            'info': 0
        }

        for poc in self.yaml_data:
            info = poc.get('info', {})
            if isinstance(info, dict):
                severity = info.get('severity', '').lower()
                if severity in stats:
                    stats[severity] += 1

        return stats

    def initUI(self):
        layout = QVBoxLayout()

        # 统计信息面板
        stats_panel = QHBoxLayout()
        stats = self.calculate_statistics()

        stats_text = (
            f"总POC数量: {stats['total']} | "
            f"严重POC: {stats['critical']} | "
            f"高危POC: {stats['high']} | "
            f"中危POC: {stats['medium']} | "
            f"低危POC: {stats['low']} | "
            f"信息POC: {stats['info']}"
        )
        stats_label = QLabel(stats_text)
        stats_label.setStyleSheet("""
            QLabel {
                background-color: #f0f0f0;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        stats_panel.addWidget(stats_label)
        layout.addLayout(stats_panel)

        # 搜索组件
        self.search_widget = SearchWidget()
        self.search_widget.set_parent(self)
        layout.addWidget(self.search_widget)

        # POC表格
        self.table = QTableWidget()
        self.setup_table()
        layout.addWidget(self.table)

        # 分页控件
        self.pagination = Pagination()
        self.pagination.pageChanged.connect(self.on_page_changed)
        layout.addWidget(self.pagination)

        # 标签统计面板
        self.tags_panel = self.create_tags_panel()
        layout.addWidget(self.tags_panel)

        self.setLayout(layout)
        self.update_pagination()

    def setup_table(self):
        headers = ['选择', '序号', '文件名', '危害', '作者', 'tags', 'CVE编号', '参考链接', '漏洞描述']
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        # 设置表格样式
        self.table.setStyleSheet("""
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

        # 设置列宽
        column_widths = [50, 40, 255, 60, 100, 160, 106, 310, None]
        for i, width in enumerate(column_widths):
            if width is not None:
                self.table.setColumnWidth(i, width)

        # 设置表格自适应
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)

        # 启用右键菜单
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)

        self.populate_table()

    def show_context_menu(self, pos):
        item = self.table.itemAt(pos)
        if not item:
            return

        row = item.row()
        menu = QMenu(self)

        # 创建菜单项
        view_action = menu.addAction("查看")
        edit_action = menu.addAction("编辑")
        delete_action = menu.addAction("删除")
        menu.addSeparator()
        copy_path_action = menu.addAction("复制文件路径")
        open_folder_action = menu.addAction("打开所在文件夹")

        # 显示菜单
        action = menu.exec_(QCursor.pos())

        if not action:
            return

        # 获取当前POC文件信息
        data = self.filtered_yaml_data if self.filtered_yaml_data else self.yaml_data
        poc = data[row]
        file_path = poc.get('full_path', '')

        # 处理菜单动作
        if action == view_action:
            self.view_poc(poc)
        elif action == edit_action:
            self.edit_poc(poc)
        elif action == delete_action:
            self.delete_poc(poc)
        elif action == copy_path_action:
            self.copy_file_path(file_path)
        elif action == open_folder_action:
            self.open_containing_folder(file_path)

    def view_poc(self, poc):
        self.pocSelected.emit(poc.get('full_path', ''))

    def edit_poc(self, poc):
        self.pocSelected.emit(poc.get('full_path', ''))

    def delete_poc(self, poc):
        file_path = poc.get('full_path', '')
        if not file_path or not os.path.exists(file_path):
            return

        reply = QMessageBox.question(
            self, '确认删除',
            f"确定要删除文件 {os.path.basename(file_path)} 吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                os.remove(file_path)
                self.yaml_data.remove(poc)
                if poc in self.filtered_yaml_data:
                    self.filtered_yaml_data.remove(poc)
                self.populate_table()
                self.update_pagination()
                QMessageBox.information(self, "成功", "文件已成功删除")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"删除文件失败：{str(e)}")

    def copy_file_path(self, file_path):
        if file_path:
            QApplication.clipboard().setText(file_path)

    def open_containing_folder(self, file_path):
        if not file_path:
            return

        folder_path = os.path.dirname(file_path)
        if sys.platform == 'win32':
            os.startfile(folder_path)
        elif sys.platform == 'darwin':
            subprocess.run(['open', folder_path])
        else:
            subprocess.run(['xdg-open', folder_path])

    def create_tags_panel(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMaximumHeight(150)

        container = QWidget()
        grid = QGridLayout()

        # 统计标签
        all_tags = []
        for poc in self.yaml_data:
            info = poc.get('info', {})
            if isinstance(info, dict):
                tags = info.get('tags', [])
                if isinstance(tags, str):
                    tags = [tag.strip() for tag in tags.split(',')]
                elif isinstance(tags, list):
                    all_tags.extend(tag.strip() for tag in tags if tag)

        # 获取出现次数前100的标签
        tag_counter = Counter(all_tags)
        top_tags = tag_counter.most_common(100)

        # 创建标签卡片
        row = 0
        col = 0
        for tag, count in top_tags:
            tag_button = QPushButton(f"{tag} ({count})")
            tag_button.setStyleSheet("""
                QPushButton {
                    background-color: #e1e1e1;
                    border-radius: 5px;
                    padding: 5px;
                    margin: 2px;
                }
                QPushButton:hover {
                    background-color: #d1d1d1;
                }
            """)
            tag_button.clicked.connect(lambda checked, t=tag: self.filter_by_tag(t))

            grid.addWidget(tag_button, row, col)
            col += 1
            if col >= 10:  # 每行显示10个标签
                col = 0
                row += 1

        container.setLayout(grid)
        scroll.setWidget(container)
        return scroll

    def filter_by_tag(self, tag):
        self.filtered_yaml_data = [
            poc for poc in self.yaml_data
            if tag in (poc.get('info', {}).get('tags', [])
                       if isinstance(poc.get('info', {}).get('tags', []), list)
                       else str(poc.get('info', {}).get('tags', '')).split(','))
        ]
        self.current_page = 1
        self.populate_table()
        self.update_pagination()

    def update_pagination(self):
        data = self.filtered_yaml_data if self.filtered_yaml_data else self.yaml_data
        total_pages = (len(data) + self.rows_per_page - 1) // self.rows_per_page
        self.pagination.set_total_pages(total_pages)

    def on_page_changed(self, page):
        self.current_page = page
        self.populate_table()

    def populate_table(self):
        data = self.filtered_yaml_data if self.filtered_yaml_data else self.yaml_data
        start_idx = (self.current_page - 1) * self.rows_per_page
        end_idx = min(start_idx + self.rows_per_page, len(data))

        self.table.setRowCount(end_idx - start_idx)

        severity_colors = {
            'critical': QColor('#FF0000'),  # 红色
            'high': QColor('#FF4500'),  # 橙红色
            'medium': QColor('#FFA500'),  # 橙色
            'low': QColor('#FFD700'),  # 金色
            'info': QColor('#4169E1')  # 蓝色
        }

        for row, idx in enumerate(range(start_idx, end_idx)):
            poc = data[idx]
            info = poc.get('info', {}) or {}

            # 选择框
            checkbox = QCheckBox()
            checkbox.setChecked(poc.get('original_filename', '') in self.selected_pocs)
            self.table.setCellWidget(row, 0, checkbox)

            # 序号
            self.table.setItem(row, 1, QTableWidgetItem(str(idx + 1)))

            # 文件名
            filename_item = QTableWidgetItem(poc.get('original_filename', ''))
            self.table.setItem(row, 2, filename_item)

            # 危害等级
            severity = info.get('severity', '').lower()
            severity_item = QTableWidgetItem(severity)
            if severity in severity_colors:
                severity_item.setForeground(severity_colors[severity])
            self.table.setItem(row, 3, severity_item)

            # 作者
            self.table.setItem(row, 4, QTableWidgetItem(info.get('author', '')))

            # 标签
            tags = info.get('tags', [])
            if isinstance(tags, list):
                tags = ', '.join(str(tag) for tag in tags if tag)
            elif isinstance(tags, str):
                tags = tags.strip()
            self.table.setItem(row, 5, QTableWidgetItem(str(tags)))

            # CVE编号
            classification = info.get('classification', {}) or {}
            cve = classification.get('cve-id', '')
            self.table.setItem(row, 6, QTableWidgetItem(str(cve)))

            # 参考链接
            reference = info.get('reference', [])
            if reference:
                if isinstance(reference, list):
                    reference = ', '.join(str(ref) for ref in reference if ref)
                elif isinstance(reference, str):
                    reference = reference.strip()
                else:
                    reference = str(reference)
            else:
                reference = ''
            self.table.setItem(row, 7, QTableWidgetItem(reference))

            # 漏洞描述
            description = info.get('description', '')
            self.table.setItem(row, 8, QTableWidgetItem(str(description)))


# 更新 StatsTab 类中的搜索相关方法
def search_table(self, keyword):
    """使用关键词搜索POC"""
    if not keyword:
        self.reset_search()
        return

    # 分割搜索关键词
    keywords = keyword.split()

    # 处理逻辑运算符
    if '&&' in keywords:
        # AND 操作
        keywords.remove('&&')
        self.filtered_yaml_data = [
            item for item in self.yaml_data
            if all(self._search_in_item(item, kw) for kw in keywords)
        ]
    elif '||' in keywords:
        # OR 操作
        keywords.remove('||')
        self.filtered_yaml_data = [
            item for item in self.yaml_data
            if any(self._search_in_item(item, kw) for kw in keywords)
        ]
    else:
        # 默认为 AND 操作
        self.filtered_yaml_data = [
            item for item in self.yaml_data
            if all(self._search_in_item(item, kw) for kw in keywords)
        ]

    # 更新表格和分页
    self.current_page = 1
    self.populate_table()
    self.update_pagination()


def _search_in_item(self, item, keyword):
    """在POC数据中搜索关键词"""
    keyword = keyword.lower()

    # 搜索文件名
    if keyword in str(item.get('original_filename', '')).lower():
        return True

    # 搜索info字段
    info = item.get('info', {})
    if isinstance(info, dict):
        # 搜索标题
        if keyword in str(info.get('name', '')).lower():
            return True

        # 搜索作者
        if keyword in str(info.get('author', '')).lower():
            return True

        # 搜索描述
        if keyword in str(info.get('description', '')).lower():
            return True

        # 搜索标签
        tags = info.get('tags', [])
        if isinstance(tags, list):
            if any(keyword in str(tag).lower() for tag in tags):
                return True
        elif isinstance(tags, str):
            if keyword in tags.lower():
                return True

        # 搜索CVE编号
        classification = info.get('classification', {})
        if isinstance(classification, dict):
            if keyword in str(classification.get('cve-id', '')).lower():
                return True

    # 搜索整个YAML内容
    return keyword in str(item).lower()


def reset_search(self):
    """重置搜索结果"""
    self.filtered_yaml_data = []
    self.current_page = 1
    self.populate_table()
    self.update_pagination()