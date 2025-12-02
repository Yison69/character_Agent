# src/core/llm_engine.py
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# 修改为你的实际模型路径
MODEL_PATH = "/data/huangyisong/character_AI/weights/qwen/Qwen3-8B"

class LocalLLMEngine:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print(f"🚀 [System] 正在加载模型权重: {MODEL_PATH} ...")
            cls._instance = super(LocalLLMEngine, cls).__new__(cls)
            cls._instance.tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
            cls._instance.model = AutoModelForCausalLM.from_pretrained(
                MODEL_PATH,
                device_map="auto",
                torch_dtype=torch.bfloat16,
                trust_remote_code=True
            )
            print("✅ [System] 模型加载完毕，引擎就绪。")
        return cls._instance

    def generate(self, prompt: str, max_tokens=512, temperature=0.3):
        """通用生成函数"""
        messages = [{"role": "user", "content": prompt}]
        
        # 构建 Chat 格式输入
        text = self.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

        with torch.no_grad():
            generated_ids = self.model.generate(
                **model_inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=(temperature > 0)
            )
        
        # 截取新生成的 tokens
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return response.strip()

# 全局单例对象
engine = LocalLLMEngine()