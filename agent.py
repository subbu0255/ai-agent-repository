import os
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_groq import ChatGroq
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from tools import (
    check_device_status,
    get_cpu_usage,
    get_memory_usage,
    get_disk_usage,
    get_battery_status,
    create_service_ticket,
)

load_dotenv()

TOOLS = [
    check_device_status,
    get_cpu_usage,
    get_memory_usage,
    get_disk_usage,
    get_battery_status,
    create_service_ticket,
]

SYSTEM_PROMPT = """You are a Mac IT Support Agent.

Your job is to diagnose an employee's Mac when they report a performance problem.

You have these tools:
- check_device_status
- get_cpu_usage
- get_memory_usage
- get_disk_usage
- get_battery_status
- create_service_ticket

Important rules:
1. Use real device tools when the employee asks you to inspect or diagnose the Mac.
2. Do not invent metrics.
3. CPU >= 90% or memory >= 90% is considered high usage for this classroom POC.
4. Disk usage >= 90% is considered high.
5. A battery problem can be reported if the battery health/status tool indicates one.
6. Do not create a ticket merely because the user says the Mac is slow.
7. If a meaningful problem is found, ask for confirmation before creating a REAL ticket.
8. If the user explicitly says they want a ticket created, you may call create_service_ticket().
9. Explain which real metrics caused the recommendation.
10. Never claim a real ticket was created unless the tool actually returned a ticket ID.

This is a teaching POC. The device diagnostic tools are REAL local Mac measurements.
The ticket tool is intentionally a SAFE local ticket simulation unless a real ITSM integration is added.
"""

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Copy .env.example to .env and add your Groq API key."
        )

    model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    return ChatGroq(
        model=model,
        temperature=0,
        api_key=api_key,
    ).bind_tools(TOOLS)


llm = get_llm()


def agent_node(state: AgentState):
    response = llm.invoke(
        [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    )
    return {"messages": [response]}


tool_node = ToolNode(TOOLS)


def should_continue(state: AgentState):
    last = state["messages"][-1]

    if getattr(last, "tool_calls", None):
        return "tools"

    return END


graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue)
graph.add_edge("tools", "agent")

app = graph.compile()


def run_agent(user_request: str) -> str:
    result = app.invoke({
        "messages": [HumanMessage(content=user_request)]
    })

    print("---- REAL DEVICE AGENT TRACE ----")

    for message in result["messages"]:
        if getattr(message, "tool_calls", None):
            for call in message.tool_calls:
                print(f"Tool selected: {call['name']}({call['args']})")

        elif isinstance(message, ToolMessage):
            print(f"Tool result: {message.content}")

    print("----------------------------------")

    return result["messages"][-1].content
