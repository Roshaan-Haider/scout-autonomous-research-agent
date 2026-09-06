from graph.agent_graph import app

def run_agent(question: str):
    result = app.invoke(
        {
            "messages": [("user", question)],
            "tool_calls_made": 0
        },
        config={"recursion_limit": 15}
    )
    return result["messages"][-1].content

if __name__ == "__main__":
    print("Scout — Autonomous Research Agent")
    print("Ask a research question, or type 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()
        if question.lower() in ("exit", "quit"):
            print("Goodbye.")
            break
        if not question:
            continue

        print("\nScout is researching...\n")
        answer = run_agent(question)
        print(f"Scout: {answer}\n")