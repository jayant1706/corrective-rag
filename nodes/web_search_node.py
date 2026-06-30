from tavily import TavilyClient
from config import TAVILY_API_KEY

client = TavilyClient(api_key=TAVILY_API_KEY)


def web_search(state):

    print("\n========== WEB SEARCH ==========\n")

    question = state["question"]

    response = client.search(
        query=question,
        search_depth="advanced",
        max_results=5,
    )

    context = ""

    for i, result in enumerate(response["results"], start=1):
        context += f"""
Result {i}

Title:
{result['title']}

URL:
{result['url']}

Content:
{result['content']}

-------------------------
"""

    return {
        "web_context": context
    }