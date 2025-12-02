def memory_node(state: dict):
    """
    【记忆形成器模块】
    负责从对话历史中提取关键信息，或从向量数据库中检索长期记忆。
    
    在 Demo 阶段，我们先返回一个默认值。
    未来可以在这里接入 LlamaIndex 的检索逻辑。
    """
    # 这里的 state["chat_history"] 是之前的对话列表
    # 你可以在这里写逻辑来总结对话摘要
    
    return {"retrieved_memory": "（暂无特殊长期记忆）"}