from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                           QPlainTextEdit, QLineEdit, QCheckBox, QPushButton)
from ...utils.nuclei_runner import NucleiRunner

class RunnerTab(QWidget):
    def __init__(self, yaml_data, yaml_folder_path):
        super().__init__()
        self.yaml_data = yaml_data
        self.nuclei_runner = NucleiRunner(yaml_folder_path)
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        # Target input
        target_layout = QVBoxLayout()
        target_layout.addWidget(QLabel("目标 (每行一个):"))
        self.target_input = QPlainTextEdit()
        target_layout.addWidget(self.target_input)
        layout.addLayout(target_layout)
        
        # Control panel
        control_layout = QHBoxLayout()
        
        # Proxy input
        proxy_layout = QHBoxLayout()
        proxy_layout.addWidget(QLabel("代理:"))
        self.proxy_input = QLineEdit()
        self.proxy_input.setPlaceholderText("http://127.0.0.1:8080")
        proxy_layout.addWidget(self.proxy_input)
        control_layout.addLayout(proxy_layout)
        
        # Options
        self.details_checkbox = QCheckBox("显示详细信息")
        control_layout.addWidget(self.details_checkbox)
        
        # Run buttons
        self.run_button = QPushButton("运行选中")
        self.run_button.clicked.connect(self.run_selected)
        control_layout.addWidget(self.run_button)
        
        self.batch_button = QPushButton("批量运行")
        self.batch_button.clicked.connect(self.run_batch)
        control_layout.addWidget(self.batch_button)
        
        layout.addLayout(control_layout)
        self.setLayout(layout)
        
    def run_selected(self):
        targets = self.target_input.toPlainText().strip()
        if not targets:
            return
            
        temp_file = self.nuclei_runner.save_targets_file(targets)
        cmd = ["nuclei", "-t", self.yaml_folder_path, "-l", temp_file]
        
        if self.details_checkbox.isChecked():
            cmd.append("--dresp")
            
        if self.proxy_input.text():
            cmd.extend(["-proxy", self.proxy_input.text()])
            
        self.nuclei_runner.execute_command(cmd, self)
        
    def run_batch(self):
        self.run_selected()  # Same logic for now, can be customized later