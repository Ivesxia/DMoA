import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, AutoModelForSeq2SeqLM

cache_path = "E:/hf_cache/clinical_camel"
model_name = "microsoft/BioGPT"

def local_model(cache_path, model_name):
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        cache_dir=cache_path,
        trust_remote_code=True
    )

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        cache_dir=cache_path,
        device_map="auto",
        trust_remote_code=True
    )

    generator = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        device_map="auto",
        torch_dtype=torch.float16
    )

    return generator, tokenizer


class LocalAgent:
    def __init__(self, model_name, cache_path, name="LocalModel", temperature=0.7):
        self.generator, self.tokenizer = local_model(cache_path, model_name)
        self.name = name
        self.temperature = temperature
        self.memory_lst = []

    def set_meta_prompt(self, meta_prompt: str):
        """设定 system 级提示词"""
        self.memory_lst.append({"role": "system", "content": meta_prompt})

    def add_event(self, event: str):
        """添加用户输入"""
        self.memory_lst.append({"role": "user", "content": event})

    def add_memory(self, memory: str):
        """添加模型回复"""
        self.memory_lst.append({"role": "assistant", "content": memory})
        print(f"----- {self.name} -----\n{memory}\n")

    def ask(self, temperature=None):
        """进行一次生成"""
        temperature = temperature if temperature is not None else self.temperature

        # 拼接所有历史对话作为 prompt
        prompt = self._format_messages_as_prompt()

        # 生成回复
        output = self.generator(
            prompt,
            max_new_tokens=256,
            do_sample=True,
            temperature=temperature
        )[0]["generated_text"]

        # 去除前缀 prompt 部分，只保留新生成内容
        generated = output[len(prompt):].strip()
        self.add_memory(generated)
        return generated

    def _format_messages_as_prompt(self):
        """将 memory 转换为 prompt 格式，适配普通文本生成模型"""
        prompt = ""
        for msg in self.memory_lst:
            role = msg["role"]
            content = msg["content"]
            if role == "system":
                prompt += f"[系统提示] {content}\n"
            elif role == "user":
                prompt += f"用户：{content}\n"
            elif role == "assistant":
                prompt += f"{self.name}：{content}\n"
        prompt += f"{self.name}："
        return prompt
    

class ClinicalT5Agent:
    def __init__(self, model_name, cache_path, temperature=0.7):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name, cache_dir=cache_path, from_flax=True)
        self.temperature = temperature
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = self.model.to(self.device)

    def ask(self, prompt: str, max_new_tokens=128):
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        output = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=self.temperature,
            do_sample=True,
            top_p=0.9
        )
        return self.tokenizer.decode(output[0], skip_special_tokens=True)
