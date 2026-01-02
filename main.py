from langgraph.graph import StateGraph, MessagesState, START, END
from ollama import Client
from IPython.display import display, Image

# langgraph node to call the LLM
def call_llm(state: MessagesState) -> str:
    try:
      print("Calling LLM...")
      print("state:", state["messages"])
      # ollama api call
      prompt = """
      You are a helpful AI assistant. Respond to the following messages:
      {messages}
      """
      ollama = Client(host="http://localhost:11434")
      response = ollama.generate(model="qwen3:8b", prompt=prompt)
      return response
    except Exception as e:
      print("Error calling LLM:", str(e))
      return "Error: Unable to get response from LLM."

def main():
    # state graph definition
    graph = StateGraph(MessagesState)

    # Add a node for calling the LLM
    graph.add_node("call_llm", call_llm)
    
    # Connect the start state to the LLM call node
    graph.add_edge(START, "call_llm")


    # Connect the LLM call node to the end state
    graph.add_edge("call_llm", END)

    # compile the graph
    graph = graph.compile()

    display(Image(graph.get_graph().draw_mermaid_png(output_file_path="simple.png")))

    result = graph.invoke(
        {"messages": [{"role": "user", "content": "Hello, how are you?"}]}
    )
    print("Result:", result)
    # while True:
    #     user_input = input("User: ")
    #     if user_input.lower() in ["exit", "quit"]:
    #         break

    #     # Execute the graph with user input
    #     response = graph.invoke(
    #         {"messages": [{"role": "user", "content": user_input}]}
    #     )
    #     print("AI:", response)

if __name__ == "__main__":
    main()