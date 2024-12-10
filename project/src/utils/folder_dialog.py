from PyQt5.QtWidgets import QApplication, QInputDialog, QMessageBox, QFileDialog
import os
import sys

def get_yaml_folder_path():
    """Get the folder path containing YAML files, including subdirectories."""
    app = QApplication.instance() or QApplication(sys.argv)
    
    while True:
        # Use QFileDialog instead of QInputDialog for better directory selection
        folder_path = QFileDialog.getExistingDirectory(
            None,
            "选择包含nuclei-poc文件的目录",
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        
        if folder_path:
            if not os.path.exists(folder_path):
                QMessageBox.warning(None, "路径错误", "指定的路径不存在，请重新选择。")
                continue
            
            # Check if there are any YAML files in the directory or its subdirectories
            yaml_files = []
            for root, _, files in os.walk(folder_path):
                yaml_files.extend([f for f in files if f.lower().endswith('.yaml')])
            
            if not yaml_files:
                reply = QMessageBox.question(
                    None,
                    "无YAML文件",
                    "所选目录及其子目录中未找到YAML文件。是否重新选择目录？",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    continue
                else:
                    QMessageBox.warning(None, "退出", "感谢使用！")
                    sys.exit()
            
            # Show summary of found files
            QMessageBox.information(
                None,
                "扫描完成",
                f"在所选目录及其子目录中找到 {len(yaml_files)} 个YAML文件。"
            )
            
            return folder_path
        else:
            reply = QMessageBox.question(
                None,
                "未选择目录",
                "您没有选择目录。是否重试？",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                QMessageBox.warning(None, "退出", "感谢使用！")
                sys.exit()