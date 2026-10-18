import time
from tavily import TavilyClient
from config import TAVILY_API_KEY
from utils.logger import logger


def web_search(state):
    start_time = time.perf_counter()
    logger.info("WEB SEARCH | Searching Tavily")

    question = state.get("rewritten_question") or state.get("question", "")
    context = ""
    web_sources = []

    if not TAVILY_API_KEY:
        logger.warning("WEB SEARCH | TAVILY_API_KEY is not configured")
        trace = list(state.get("execution_trace", []))
        step_history = list(state.get("step_history", []))
        trace.append({
            "step": "Web Search",
            "status": "skipped",
            "duration_sec": 0,
            "message": "Tavily API key not found; skipping web search fallback."
        })
        step_history.append("Web Search (Skipped)")
        return {
            "web_context": "",
            "web_sources": [],
            "execution_trace": trace,
            "step_history": step_history,
        }

    try:
        client = TavilyClient(api_key=TAVILY_API_KEY)
        response = client.search(
            query=question,
            search_depth="advanced",
            max_results=5,
        )

        results = response.get("results", [])
        for i, result in enumerate(results, start=1):
            title = result.get("title", "Untitled")
            url = result.get("url", "#")
            content = result.get("content", "")

            web_sources.append({
                "index": i,
                "title": title,
                "url": url,
                "snippet": content[:250].strip() + ("..." if len(content) > 250 else ""),
                "full_content": content
            })

            context += f"""
Result {i}
Title: {title}
URL: {url}
Content: {content}
-------------------------
"""
        logger.info(f"WEB SEARCH | Found {len(results)} results")

    except Exception as e:
        logger.error(f"WEB SEARCH | Tavily search failed: {e}")
        context = ""

    duration = round(time.perf_counter() - start_time, 3)

    trace = list(state.get("execution_trace", []))
    step_history = list(state.get("step_history", []))

    trace.append({
        "step": "Web Search",
        "status": "success" if web_sources else "warning",
        "duration_sec": duration,
        "message": f"Tavily returned {len(web_sources)} external web results for: '{question}'",
        "count": len(web_sources),
        "query": question
    })
    step_history.append(f"Web Search ({len(web_sources)} results)")

    return {
        "web_context": context,
        "web_sources": web_sources,
        "active_route": "web_augmented",
        "execution_trace": trace,
        "step_history": step_history,
    }