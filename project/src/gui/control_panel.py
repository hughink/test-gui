from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QLineEdit, 
                           QPushButton, QCheckBox, QPlainTextEdit)

class ControlPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()
        
    def initUI(self):
        layout = QHBoxLayout()
        
        # Target input label
        target_label = QLabel("Enter targets (one per line):")
        layout.addWidget(target_label)
        
        # Target input
        self.target_input = QPlainTextEdit()
        self.target_input.setMaximumHeight(50)
        layout.addWidget(self.target_input)
        
        # Proxy input
        proxy_label = QLabel("Proxy:")
        layout.addWidget(proxy_label)
        
        self.proxy_input = QLineEdit()
        self.proxy_input.setPlaceholderText("http://127.0.0.1:8080")
        layout.addWidget(self.proxy_input)
        
        # Details checkbox
        self.details_checkbox = QCheckBox("Details")
        layout.addWidget(self.details_checkbox)
        
        # Run buttons
        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self.on_run_clicked)
        layout.addWidget(self.run_button)
        
        self.batch_button = QPushButton("Batch Run")
        self.batch_button.clicked.connect(self.on_batch_run_clicked)
        layout.addWidget(self.batch_button)
        
        # Save and exit buttons
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.on_save_clicked)
        layout.addWidget(self.save_button)
        
        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.on_exit_clicked)
        layout.addWidget(self.exit_button)
        
        self.setLayout(layout)
    
    def on_run_clicked(self):
        if hasattr(self.parent, 'run_nuclei'):
            self.parent.run_nuclei()
    
    def on_batch_run_clicked(self):
        if hasattr(self.parent, 'run_nuclei_batch'):
            self.parent.run_nuclei_batch()
    
    def on_save_clicked(self):
        if hasattr(self.parent, 'save_yaml_content'):
            self.parent.save_yaml_content()
    
    def on_exit_clicked(self):
        if hasattr(self.parent, 'close'):
            self.parent.close()