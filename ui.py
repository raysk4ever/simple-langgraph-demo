import gradio as gr
from user_input_example import get_graph

def normalize_history(history):
    normalized = []
    for item in history:
        if isinstance(item, tuple):
            user, bot = item
            normalized.append({"role": "user", "content": user})
            normalized.append({"role": "assistant", "content": bot})
        else:
            normalized.append(item)
    return normalized



def chat_fn(text: str, history):
  # history = normalize_history(history)
  # messages = history + [
  #   { "role": "user", "content": text },
  #   { "role": "assistant", "content": "thinking..." }
  # ]
  # yield messages
  result = get_graph().invoke({ "user_input": text })
  print("result", result)
  return result["result"]
  # for event in result:
  #   if "result" in event:
  #     messages[-1]["content"] = event["result"]
  #     yield messages

gr.ChatInterface(
  fn=chat_fn,
  examples=[
    "C++ code for sum",
    "what can you do?",
    "Hi"
  ],
  title="Pink Bot"
).launch(
  # share=True
)
