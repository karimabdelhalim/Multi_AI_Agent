"""
graph.py
--------
Wires the Supervisor + all worker agents into a LangGraph StateGraph.
Because agents are built from agents_pkg.AGENT_SPECS, adding a new agent
there is enough to have it show up here too — no edits needed.
"""

from langgraph.graph import StateGraph, START, END

from supervisor import State, supervisor_node
from agents_pkg import build_agents, agent_names


def build_graph():
    builder = StateGraph(State)

    builder.add_node("Supervisor", supervisor_node)

    agents = build_agents()
    for name, agent in agents.items():
        builder.add_node(name, agent)

    builder.add_edge(START, "Supervisor")

    # Conditional routing: supervisor decides which agent (or FINISH) is next.
    routing_map = {name: name for name in agent_names()}
    routing_map["FINISH"] = END
    builder.add_conditional_edges("Supervisor", lambda state: state["next"], routing_map)

    # Workers always report back to the supervisor.
    for name in agent_names():
        builder.add_edge(name, "Supervisor")

    return builder.compile()
