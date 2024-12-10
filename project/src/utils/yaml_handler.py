import yaml
import hashlib
from PyQt5.QtWidgets import QMessageBox

class YamlHandler:
    @staticmethod
    def save_yaml_content(content, file_path, parent_widget=None):
        try:
            # Validate YAML content
            yaml.safe_load(content)
            
            # Save content
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
                
            return True
        except Exception as e:
            if parent_widget:
                QMessageBox.critical(parent_widget, "Save Error", f"Failed to save YAML content:\n{e}")
            return False
            
    @staticmethod
    def calculate_content_hash(content):
        return hashlib.md5(content.encode('utf-8')).hexdigest()
        
    @staticmethod
    def check_duplicate_content(content, yaml_folder_path, current_filename=None):
        content_hash = YamlHandler.calculate_content_hash(content)
        
        for filename in os.listdir(yaml_folder_path):
            if filename.lower().endswith('.yaml') and filename != current_filename:
                file_path = os.path.join(yaml_folder_path, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        existing_content = f.read()
                        if YamlHandler.calculate_content_hash(existing_content) == content_hash:
                            return True, filename
                except:
                    continue
                    
        return False, None