#!/usr/bin/env python3
import sys
import os

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from PyQt5.QtWidgets import QApplication
from src.gui.main_window import NucleiPOCManager
from src.utils.yaml_loader import load_yaml_files
from src.utils.folder_dialog import get_yaml_folder_path


def main():
    app = QApplication(sys.argv)
    yaml_folder_path = get_yaml_folder_path()
    if yaml_folder_path:
        yaml_data = load_yaml_files(yaml_folder_path)
        ex = NucleiPOCManager(yaml_data, yaml_folder_path)
        ex.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    main()
