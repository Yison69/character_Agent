import sys
import os

# 路径修复
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.graph.workflow import app

def main():
    print("========================================")
    print("🤖 Universal Character Agent Engine")
    print("========================================")
    
    # 1. 动态选择角色
    while True:
        char_id = input("\n请根据 data/personas/ 下的文件名输入角色ID (例如 sheldon): ").strip()
        if char_id:
            break
    
    print(f"🚀 正在初始化引擎，加载角色: {char_id} ...")
    
    chat_history = []
    
    # 用于记录显示名字 (从第一次运行结果中获取)
    display_name = "Agent" 
    
    while True:
        try:
            query = input("\nUser (You): ")
        except EOFError:
            break

        if query.strip().lower() in ["exit", "quit"]:
            print("Bye!")
            break
        
        if not query.strip():
            continue
            
        # 2. 构造输入，传入 character_id
        inputs = {
            "user_query": query,
            "chat_history": chat_history,
            "character_id": char_id 
        }
        
        try:
            print(f"... {display_name} 正在思考 ...")
            
            # 运行图
            result = app.invoke(inputs)
            
            # 3. 动态更新显示名字 (从加载的配置里读名字)
            if "char_config" in result and "name" in result["char_config"]:
                display_name = result["char_config"]["name"]
            
            response = result.get("final_response", "...")
            
            # 打印结果
            print(f"{display_name}: {response}")
            
            # 维护历史
            chat_history.append(f"User: {query}")
            chat_history.append(f"{display_name}: {response}")
            
        except Exception as e:
            print(f"❌ 运行出错: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()