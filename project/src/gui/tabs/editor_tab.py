from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QFileDialog)
from ..editor_widget import YamlEditor
from ...utils.yaml_handler import YamlHandler

class EditorTab(QWidget):
    def __init__(self, yaml_folder_path):
        super().__init__()
        self.yaml_folder_path = yaml_folder_path
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        # Editor
        self.editor = YamlEditor()
        layout.addWidget(self.editor)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        new_button = QPushButton("新建")
        new_button.clicked.connect(self.new_file)
        
        open_button = QPushButton("打开")
        open_button.clicked.connect(self.open_file)
        
        save_button = QPushButton("保存")
        save_button.clicked.connect(self.save_file)
        
        button_layout.addWidget(new_button)
        button_layout.addWidget(open_button)
        button_layout.addWidget(save_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
    def new_file(self):
        self.editor.clear()
        
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "打开POC文件", 
            self.yaml_folder_path,
            "YAML files (*.yaml);;All files (*.*)"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.editor.setPlainText(f.read())
            except Exception as e:
                QMessageBox.critical(self, "错误", f"无法打开文件:\n{str(e)}")
                
    def save_file(self):
        content = self.editor.toPlainText()
        if not content.strip():
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存POC文件",
            self.yaml_folder_path,
            "YAML files (*.yaml);;All files (*.*)"
        )
        if file_path:
            YamlHandler.save_yaml_content(content, file_path, self)