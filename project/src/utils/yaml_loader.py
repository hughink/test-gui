import os
import yaml
from PyQt5.QtWidgets import QMessageBox

def load_yaml_files(yaml_folder):
    """加载指定文件夹及其子文件夹中的所有YAML文件。"""
    yaml_data = []
    total_files = 0
    error_files = []
    
    for dirpath, _, files in os.walk(yaml_folder):
        for file_name in files:
            if file_name.lower().endswith('.yaml'):
                total_files += 1
                yaml_file_path = os.path.join(dirpath, file_name)
                try:
                    with open(yaml_file_path, 'r', encoding='utf-8') as yaml_file:
                        data = yaml.safe_load(yaml_file)
                        
                        # 确保数据是字典类型
                        if not isinstance(data, dict):
                            error_files.append(f"{file_name} (无效的YAML格式)")
                            continue
                            
                        # 确保info字段存在且是字典类型
                        if 'info' not in data or not isinstance(data['info'], dict):
                            error_files.append(f"{file_name} (缺少info字段或格式错误)")
                            continue
                            
                        # 存储相对路径而不是仅文件名
                        rel_path = os.path.relpath(yaml_file_path, yaml_folder)
                        data['original_filename'] = rel_path
                        data['full_path'] = yaml_file_path
                        yaml_data.append(data)
                        
                except yaml.YAMLError as e:
                    error_files.append(f"{file_name} (YAML解析错误: {str(e)})")
                except Exception as e:
                    error_files.append(f"{file_name} (读取错误: {str(e)})")
    
    # 显示加载结果摘要
    if error_files:
        error_message = "以下文件加载失败：\n\n" + "\n".join(error_files)
        QMessageBox.warning(None, "加载警告", error_message)
    
    success_message = (f"成功加载 {len(yaml_data)} 个POC文件\n"
                      f"失败 {len(error_files)} 个文件\n"
                      f"总计扫描 {total_files} 个文件")
    QMessageBox.information(None, "加载完成", success_message)
    
    return yaml_data