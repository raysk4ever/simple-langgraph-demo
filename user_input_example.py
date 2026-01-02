from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from llm import llm
from IPython.display import Image, display
from pydantic import BaseModel, Field
from typing import Literal

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate


class IntentOutput(BaseModel):
  intent: Literal["data", "general", "docs", "code", "unknown"]

intent_parser = PydanticOutputParser(pydantic_object=IntentOutput)

# Define the structure of the graph state
class GraphState(TypedDict):
    user_input: str
    intent: Literal["data", "general", "docs", "code", "unknown"]
    result: str

# A langgraph node to get user input
def get_user_input(state: GraphState) -> GraphState:
    return state

def detect_intent(state: GraphState) -> GraphState:
    print("👀 Detecting intent for user input:", state["user_input"])
    intent_prompt = PromptTemplate(
      template="""
      You are a JSON API.

      You must ONLY return a valid JSON object.
      Do NOT include explanations, markdown, or code blocks.

      {format_instructions}

      User input:
      {input}
      """,
      input_variables=["input"],
      partial_variables={
        "format_instructions": intent_parser.get_format_instructions()
      }
    )
    chain = intent_prompt | llm | intent_parser
    parsed = chain.invoke({ "input": state['user_input'] })
    print("----parsed", parsed)
    return { "intent": parsed.intent }

def router(state: GraphState) -> str:
    print("🚦 Routing based on intent:", state["intent"])
    return state["intent"]

def  code_node(state: GraphState) -> GraphState:
  print("💻 Handling code-related request.")
  prompt = f"""
  You are an AI assistant that helps with coding tasks.
  User Input: "{state['user_input']}"
  """

  result = llm.invoke(prompt)
  print("code_node", result)
  return { "result": result.content }

def general_node(state: GraphState) -> GraphState:
  print("🌐 Handling general request.")
  prompt = f"""
  You are an AI assistant that helps with general knowledge questions.
  User Input: "{state['user_input']}"
  """
  result = llm.invoke(prompt)  
  return { "result": result.content }

def data_node(state: GraphState) -> GraphState:
  print("📊 Handling data-related request.")
  prompt = f"""
  You are an AI assistant that helps with data analysis tasks.
  User Input: "{state['user_input']}"
  """
  result = llm.invoke(prompt)
  return { "result": result.content }

def docs_node(state: GraphState) -> GraphState:
  print("📚 Handling documentation-related request.")
  prompt = f"""
  You are an AI assistant that helps with documentation tasks.
  User Input: "{state['user_input']}"
  """
  result = llm.invoke(prompt)
  return { "result": result.content }

def unknown_node(state: GraphState) -> GraphState:
  print("❓ Handling unknown request.")
  return { "result": "I'm not sure how to help with that." }

def summarize_node(state: GraphState) -> GraphState:
  print("📝 Summarizing the response.")
  prompt = f"""
  You are an AI assistant that summarizes responses concisely.
  User Query: "{state['user_input']}"
  Original Response: "{state['result']}"
  """
  response = llm.invoke(prompt)
  return { "result": response }

def get_graph():
   # define the state graph
    builder = StateGraph(GraphState)

    builder.add_node("get_user_input", get_user_input)
    builder.add_node("detect_intent", detect_intent)
    builder.add_node("code_node", code_node)
    builder.add_node("general_node", general_node)
    builder.add_node("data_node", data_node)
    builder.add_node("docs_node", docs_node)
    builder.add_node("unknown_node", unknown_node)
    builder.add_node("summarize_node", summarize_node)

    # connect the nodes
    builder.add_edge(START, "get_user_input")
    builder.add_edge("get_user_input", "detect_intent")
    builder.add_conditional_edges("detect_intent", router, {
        "code": "code_node",
        "general": "general_node",
        "data": "data_node",
        "docs": "docs_node",
        "unknown": "unknown_node"
    })
    

    # builder.add_edge("detect_intent", "code_node")
    # builder.add_edge("detect_intent", "general_node")
    # builder.add_edge("detect_intent", "data_node")
    # builder.add_edge("detect_intent", "docs_node")
    # builder.add_edge("detect_intent", "unknown_node")
    
    # builder.add_edge("code_node", "summarize_node")
    # builder.add_edge("general_node", "summarize_node")
    # builder.add_edge("data_node", "summarize_node")
    # builder.add_edge("docs_node", "summarize_node")
    # builder.add_edge("unknown_node", "summarize_node")
    
    builder.add_edge("code_node", END)
    builder.add_edge("general_node", END)
    builder.add_edge("data_node", END)
    builder.add_edge("docs_node", END)
    builder.add_edge("unknown_node", END)

    # builder.add_edge("summarize_node", END)

    # compile the graph
    graph = builder.compile()
    return graph

def main():
    graph = get_graph()
    # graph.invoke()
    # print(graph.get_graph().draw_mermaid_png())
    display(Image(graph.get_graph().draw_mermaid_png(output_file_path="state_graph_condition.png")))

    # response = graph.invoke({"user_input": "Create a C++ program for adding two numbers."})
    # print("Final Response:", response["result"])


# call the main function
if __name__ == "__main__":
    main()




