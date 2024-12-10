
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QMessageBox)
from ..editor_widget import YamlEditor
from ...utils.yaml_handler import YamlHandler

class YamlEditorDialog(QDialog):
    def __init__(self, yaml_content='', parent=None):
        super().__init__(parent)
        self.yaml_content = yaml_content
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('YAML编辑器')
        self.setGeometry(100, 100, 800, 600)
        
        layout = QVBoxLayout()
        
        # 编辑器
        self.editor = YamlEditor()
        self.editor.setPlainText(self.yaml_content)
        layout.addWidget(self.editor)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        save_button = QPushButton('保存')
        save_button.clicked.connect(self.save_content)
        
        cancel_button = QPushButton('取消')
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
    def save_content(self):
        content = self.editor.toPlainText()
        try:
            # 验证YAML格式
            YamlHandler.validate_yaml(content)
            self.yaml_content = content
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, '保存失败', f'YAML格式错误:\n{str(e)}')
