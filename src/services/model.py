import torch
from transformers import pipeline

model_id = "meta-llama/Llama-3.2-1B"

pipe = pipeline("text-generation", model=model_id, torch_dtype=torch.bfloat16, device_map="auto", max_new_tokens=200)


def generate_reply(message):
    prompt = f"Responde a mensagem abaixo em portugues brasil\n{message}"
    print("> Prompt:", prompt)
    
    res = pipe(prompt)
    if not res:
        return None

    generated_text = res[0].get("generated_text")
    print("> Model reply:", generated_text)
    return generated_text
