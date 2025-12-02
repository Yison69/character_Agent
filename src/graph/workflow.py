# src/graph/workflow.py

import json
from typing import TypedDict, List, Annotated, Dict, Any
import operator
from langgraph.graph import StateGraph, END

# 导入所有节点
from src.modules.state_judge import state_judge_node
from src.modules.env_judge import env_judge_node
from src.modules.memory_maker import memory_node
from src.modules.main_brain import main_brain_node
# 引入刚刚写的管理器
from src.modules.profile_manager import profile_manager

# 1. 修改 State 定义：增加通用字段
class AgentState(TypedDict):
    # --- 输入 ---
    user_query: str
    character_id: str   # <--- 新增：由 run_demo 传入
    
    # --- 动态配置 ---
    char_config: Dict[str, Any] # <--- 新增：存放加载后的 JSON 数据
    
    # --- 历史与中间态 ---
    chat_history: Annotated[List[str], operator.add]
    static_profile: str
    current_mood: str
    current_env: str
    retrieved_memory: str
    final_response: str

# 2. 重写 static_profile_node (不再返回死数据)
def static_profile_node(state: AgentState):
    char_id = state["character_id"]
    print(f"📚 [System] 正在加载角色配置: {char_id}...")
    
    # 动态加载 JSON
    config = profile_manager.load_persona(char_id)
    
    # 提取 bio_text 作为静态侧写 (假设 JSON 里有这个字段，或者动态拼装)
    # 这里为了简单，假设 JSON 里直接有一个 formatted_bio 字段，或者我们现场拼
    bio = f"姓名: {config.get('name')}\n设定: {json.dumps(config.get('bio_data', {}), ensure_ascii=False)}"
    
    return {
        "char_config": config,  # 将配置存入 State，供其他节点使用
        "static_profile": bio
    }

# 3. 构建图 (和之前一样，不用变)
workflow = StateGraph(AgentState)
workflow.add_node("profile", static_profile_node)
workflow.add_node("state_detect", state_judge_node)
workflow.add_node("env_detect", env_judge_node)
workflow.add_node("memory_proc", memory_node)
workflow.add_node("brain", main_brain_node)

workflow.set_entry_point("profile")
workflow.add_edge("profile", "state_detect")
workflow.add_edge("state_detect", "env_detect")
workflow.add_edge("env_detect", "memory_proc")
workflow.add_edge("memory_proc", "brain")
workflow.add_edge("brain", END)

app = workflow.compile()