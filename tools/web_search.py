import os
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain.tools import tool

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """Search the web for current, real-world information on a given query.
    Use this when you need facts, news, or information that might not be
    in your training data — especially anything recent or specific."""
    results = client.search(query, max_results=3)
    formatted = "\n\n".join(
        f"Source: {r['url']}\n{r['content']}"
        for r in results["results"]
    )
    return formatted

if __name__ == "__main__":
    print(web_search.invoke("What is LangGraph?"))