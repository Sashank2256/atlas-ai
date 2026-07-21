import ollama

MODEL = "qwen2.5-coder:7b"


def chat_with_ai(message: str) -> str:
    response = ollama.chat(model=MODEL, messages=[{"role": "user", "content": message}])

    return response["message"]["content"]
