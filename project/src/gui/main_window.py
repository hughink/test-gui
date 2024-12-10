from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout
from src.gui.tabs import StatsTab, EditorTab, RunnerTab
from src.gui.components import StatusBar
from src.config import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT

class NucleiPOCManager(QMainWindow):
    def __init__(self, yaml_data, yaml_folder_path):
        super().__init__()
        self.yaml_data = yaml_data
        self.yaml_folder_path = yaml_folder_path
        self.filtered_yaml_data = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Create main widget and layout
        main_widget = QWidget()
        layout = QVBoxLayout()
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Create tabs
        self.stats_tab = StatsTab(self.yaml_data)
        self.editor_tab = EditorTab(self.yaml_folder_path)
        self.runner_tab = RunnerTab(self.yaml_data, self.yaml_folder_path)
        
        # Add tabs
        self.tab_widget.addTab(self.stats_tab, "统计分析")
        self.tab_widget.addTab(self.editor_tab, "POC编辑")
        self.tab_widget.addTab(self.runner_tab, "POC执行")
        
        # Add tab widget to layout
        layout.addWidget(self.tab_widget)
        
        # Create and set status bar
        self.status_bar = StatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.update_poc_count(len(self.yaml_data))
        
        # Set layout
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)