import json
import os

class ProfileManager:
    def __init__(self):
        # 假设 JSON 文件存在项目根目录的 data/personas 下
        # 获取当前脚本的上两级目录 (modules -> src -> project_root)
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.personas_dir = os.path.join(root_dir, "data", "personas")

    def load_persona(self, char_id: str):
        file_path = os.path.join(self.personas_dir, f"{char_id}.json")
        
        if not os.path.exists(file_path):
            print(f"❌ 警告：找不到角色配置文件 {file_path}")
            # 返回一个默认的空配置，防止程序崩溃
            return {
                "name": "Unknown",
                "bio_data": {"traits": [], "profession": "Unknown"},
                "system_prompt_template": "You are a helpful assistant."
            }
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ 读取配置文件出错: {e}")
            return {}

# 单例实例
profile_manager = ProfileManager()