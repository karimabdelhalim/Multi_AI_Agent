"""
main.py
-------
CLI entrypoint. Run with: python main.py
"""

from langchain_core.messages import HumanMessage

from graph import build_graph

multi_agent = build_graph()


def main():
    print("🤖 Multi-Agent System Ready! Ask about Gold, News, Weather, or Crypto. (Type 'quit' to exit)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ("quit", "exit", "q"):
            break

        print("\n⏳ Agents are collaborating...\n")

        config = {"recursion_limit": 15}
        for event in multi_agent.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config,
            stream_mode="values",
        ):
            if "messages" not in event:
                continue

            last_message = event["messages"][-1]

            if "next" in event and event.get("next") != "FINISH":
                print(f"👉 Supervisor routing to: {event['next']}")

            if getattr(last_message, "tool_calls", None):
                for tc in last_message.tool_calls:
                    print(f"   🔧 Calling Tool: {tc['name']}")
            elif getattr(last_message, "content", None) and last_message.type == "ai":
                agent_name = getattr(last_message, "name", None) or "Worker"
                if agent_name != "Supervisor":
                    print(f"💬 {agent_name} Response: {last_message.content}\n")


if __name__ == "__main__":
    main()
