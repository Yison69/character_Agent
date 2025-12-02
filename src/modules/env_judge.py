import re
from src.core.llm_engine import engine
from src.config.prompts import ENV_JUDGE_PROMPT

def clean_output(text):
    """清洗 <think> 标签"""
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    text = text.replace('**', '').replace('【', '').replace('】', '')
    return text.strip()

def env_judge_node(state: dict):
    """
    【环境判断模块 - 通用版】
    动态读取角色配置中的 valid_locations 进行判断
    """
    query = state["user_query"]
    
    # --- 核心修改：从 State 中获取配置 ---
    config = state.get("char_config", {})
    
    # 获取可选地点列表
    valid_locations = config.get("valid_locations", ["未知地点"])
    valid_locations_str = ", ".join(valid_locations)
    # ----------------------------------
    
    prompt = ENV_JUDGE_PROMPT.format(
        valid_locations=valid_locations_str,
        query=query
    )
    
    raw_response = engine.generate(prompt, max_tokens=1024, temperature=0.1)
    env = clean_output(raw_response)
    
    if env:
        print(f"🌍 [Env Judge] 检测到地点: {env}")
        return {"current_env": env}
    else:
        print(f"⚠️ [Env Judge] 解析失败，原始输出: {raw_response[:50]}...")
        return {"current_env": valid_locations[0] if valid_locations else "未知地点"}