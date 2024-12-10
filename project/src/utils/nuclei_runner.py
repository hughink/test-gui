import os
import uuid
import shutil
import subprocess
import sys
from PyQt5.QtWidgets import QMessageBox

class NucleiRunner:
    def __init__(self, yaml_folder_path):
        self.yaml_folder_path = yaml_folder_path
        self.temp_dirs = []
        
    def save_targets_file(self, targets):
        parent_dir = os.path.dirname(self.yaml_folder_path)
        temp_file_path = os.path.join(parent_dir, "targets.txt")
        with open(temp_file_path, 'w') as file:
            file.write(targets)
        return temp_file_path
        
    def execute_command(self, cmd, parent_widget=None):
        try:
            if sys.platform == 'win32':
                subprocess.Popen(["start", "cmd", "/k"] + cmd, shell=True)
            elif sys.platform == 'darwin':
                escaped_command = ' '.join(cmd)
                script = f'tell application "Terminal" to do script "{escaped_command}"'
                subprocess.Popen(['osascript', '-e', script])
            elif sys.platform == 'linux':
                terminal_cmd = ' '.join(cmd)
                subprocess.Popen(['x-terminal-emulator', '-e', f'bash -c "{terminal_cmd}; exec bash"'])
        except Exception as e:
            if parent_widget:
                QMessageBox.critical(parent_widget, "Error", f"Command execution failed:\n{e}")
            
    def cleanup_temp_dir(self, temp_dir_path):
        if os.path.exists(temp_dir_path):
            shutil.rmtree(temp_dir_path)
        if temp_dir_path in self.temp_dirs:
            self.temp_dirs.remove(temp_dir_path)