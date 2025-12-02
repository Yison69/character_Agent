from src.modules.profile_manager import profile_manager

def static_profile_node(state: dict):
    char_id = state["character_id"]
    print(f"🔄 正在加载角色配置: {char_id}...")
    
    # 1. 加载 JSON 配置
    config = profile_manager.load_persona(char_id)
    
    # 2. (进阶) 如果需要 RAG，这里根据 config['rag_collection_name'] 连接不同的向量库
    # vector_store = get_vector_store(config['rag_collection_name'])
    # rag_info = vector_store.query(state['user_query'])
    
    return {
        "char_config": config, 
        # "static_profile": rag_info # 如果有 RAG
    }