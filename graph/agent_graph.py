from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from tools.web_search import web_search
from tools.rag_retriever import rag_retriever

MAX_TOOL_CALLS = 3

SYSTEM_PROMPT = """You are a research assistant with access to a knowledge base 
of SEC filings and web search. When answering:
- Only state facts that are explicitly present in the tool results you received.
- If the retrieved content does not contain the answer, say so clearly — do not 
  guess, infer, or fabricate specific details like names, numbers, or dates.
- It is always better to say "this information was not found in the available 
  sources" than to provide a plausible-sounding but unverified answer."""

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    tool_calls_made: int
    call_history: list

tools = [web_search, rag_retriever]
tools_by_name = {t.name: t for t in tools}

llm = ChatOpenAI(
    base_url="http://localhost:1234/v1",
    api_key="not-needed",
    model="llama-3.1-8b-instruct",
    temperature=0.7,
)
llm_with_tools = llm.bind_tools(tools)

def normalize(query: str) -> str:
    return query.strip().lower()

def agent_node(state: AgentState):
    messages = state["messages"]
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def tools_node(state: AgentState):
    last_message = state["messages"][-1]
    history = state.get("call_history", [])
    new_history = list(history)
    result_messages = []

    for call in last_message.tool_calls:
        query = call["args"].get("query", "")
        key = (call["name"], normalize(query))

        if key in history:
            result_messages.append(ToolMessage(
                content=f"You already searched for '{query}' with this tool and got a result. "
                        f"Repeating the same search will not help — try a meaningfully different "
                        f"query, use a different tool, or answer with what you already have.",
                tool_call_id=call["id"]
            ))
        else:
            tool_fn = tools_by_name[call["name"]]
            output = tool_fn.invoke(call["args"])
            result_messages.append(ToolMessage(content=output, tool_call_id=call["id"]))
            new_history.append(key)

    new_count = state.get("tool_calls_made", 0) + 1
    return {
        "messages": result_messages,
        "tool_calls_made": new_count,
        "call_history": new_history
    }

def route_after_agent(state: AgentState):
    last_message = state["messages"][-1]
    if not last_message.tool_calls:
        return END
    if state.get("tool_calls_made", 0) >= MAX_TOOL_CALLS:
        return "force_answer"
    return "tools"

def force_answer_node(state: AgentState):
    limit_notice = HumanMessage(
        content="You've reached the tool call limit. Answer using only the information you've already gathered."
    )
    response = llm.invoke(state["messages"] + [limit_notice])
    return {"messages": [response]}

graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_node("tools", tools_node)
graph.add_node("force_answer", force_answer_node)

graph.set_entry_point("agent")
graph.add_conditional_edges("agent", route_after_agent, {
    "tools": "tools",
    "force_answer": "force_answer",
    END: END
})
graph.add_edge("tools", "agent")
graph.add_edge("force_answer", END)

app = graph.compile()