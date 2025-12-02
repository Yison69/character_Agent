import re
from src.core.llm_engine import engine
from src.config.prompts import STATE_JUDGE_PROMPT

def clean_output(text):
    """清洗 <think> 标签，只保留最终结论"""
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    text = text.replace('**', '').replace('【', '').replace('】', '')
    return text.strip()

def state_judge_node(state: dict):
    """
    【状态判断模块 - 通用版】
    动态读取角色配置中的 valid_states 进行判断
    """
    query = state["user_query"]
    history = state.get("chat_history", [])[-3:]
    
    # --- 核心修改：从 State 中获取配置 ---
    config = state.get("char_config", {})
    name = config.get("name", "Agent")
    
    # 获取可选状态列表，如果 JSON 里没写，给个默认值防止报错
    valid_states = config.get("valid_states", ["平静", "开心", "生气"])
    valid_states_str = ", ".join(valid_states)
    # ----------------------------------
    
    # 注入变量到模板
    prompt = STATE_JUDGE_PROMPT.format(
        name=name,
        valid_states=valid_states_str,
        query=query, 
        history=history
    )
    
    raw_response = engine.generate(prompt, max_tokens=1024, temperature=0.1)
    mood = clean_output(raw_response)
    
    if mood:
        print(f"🧠 [State Judge] 检测到情绪: {mood}")
        return {"current_mood": mood}
    else:
        print(f"⚠️ [State Judge] 解析失败，原始输出: {raw_response[:50]}...")
        # 兜底返回列表里的第一个状态
        return {"current_mood": valid_states[0] if valid_states else "平静"}