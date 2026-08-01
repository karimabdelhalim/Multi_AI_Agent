"""
supervisor.py
-------------
The routing "manager" node. Its prompt is generated from agents_pkg.AGENT_SPECS
so it automatically knows about every agent you register there.
"""

from typing import Annotated
from typing_extensions import TypedDict

from langchain_core.messages import SystemMessage
from langgraph.graph.message import add_messages

from config import get_llm
from agents_pkg import AGENT_SPECS, agent_names


class State(TypedDict):
    messages: Annotated[list, add_messages]
    next: str


_llm = get_llm()


def _routing_prompt() -> str:
    lines = ["You are a supervisor managing the following specialist agents:"]
    for spec in AGENT_SPECS:
        lines.append(f"- '{spec['name']}_Agent': {spec['system_prompt']}")
    lines.append(
        "\nRoute to the single most relevant agent above for the user's request.\n"
        "Route to 'FINISH' if the user's question is fully answered, if the "
        "worker already attempted and failed, or if no tool is needed.\n"
        f"Respond with EXACTLY one word: one of {', '.join(agent_names())}, or FINISH."
    )
    return "\n".join(lines)


def supervisor_node(state: State):
    """The manager that decides which worker to route to."""
    system_prompt = SystemMessage(content=_routing_prompt())
    messages = [system_prompt] + state["messages"]

    response = _llm.invoke(messages)
    content = response.content.strip()

    for name in agent_names():
        if name in content:
            return {"next": name}
    return {"next": "FINISH"}
