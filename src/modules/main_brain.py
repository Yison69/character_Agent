from src.core.llm_engine import engine
from src.config.prompts import MAIN_AGENT_PROMPT

def main_brain_node(state: dict):
    """
    【主大脑模块 - 通用版】
    汇聚所有信息，生成符合当前人设的回复
    """
    # 1. 提取配置
    config = state.get("char_config", {})
    bio = config.get("bio_data", {})
    
    name = config.get("name", "Unknown Agent")
    
    # 将列表转为字符串，方便显示
    traits = ", ".join(bio.get("traits", []))
    profession = bio.get("profession", "未知职业")
    catchphrases = ", ".join(bio.get("catchphrases", []))
    
    # 2. 填入模板
    prompt = MAIN_AGENT_PROMPT.format(
        name=name,
        traits=traits,
        profession=profession,
        catchphrases=catchphrases,
        
        env=state["current_env"],
        mood=state["current_mood"],
        memory=state["retrieved_memory"],
        
        history=state.get("chat_history", []),
        query=state["user_query"]
    )
    
    # 3. 生成
    response = engine.generate(prompt, max_tokens=512, temperature=0.7)
    return {"final_response": response}
