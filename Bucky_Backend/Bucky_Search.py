import os
import asyncio
from dotenv import load_dotenv
from googleapiclient.discovery import build

# Load environment variables
load_dotenv(".env.local")

GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")


async def perform_search(query: str, num_results: int = 3) -> str:
    """
    Perform Google Custom Search in an async-safe way.
    Designed for LiveKit Agents (non-blocking).
    """

    if not GOOGLE_SEARCH_API_KEY or not SEARCH_ENGINE_ID:
        print("[ERROR] Missing Google Search API key or Search Engine ID")
        return "Sir, my search system is currently offline."

    print("\n===== Google Search Started =====")
    print(f"Query       : {query}")
    print(f"Max results : {num_results}")
    print("================================\n")

    loop = asyncio.get_running_loop()

    def _sync_search():
        """Synchronous search function to run in executor"""
        try:
            service = build(
                "customsearch",
                "v1",
                developerKey=GOOGLE_SEARCH_API_KEY,
                cache_discovery=False,
            )
            
            result = service.cse().list(
                q=query,
                cx=SEARCH_ENGINE_ID,
                num=num_results,
            ).execute()
            
            return result
        except Exception as e:
            print(f"[ERROR] Search execution failed: {e}")
            raise

    try:
        # Run the synchronous search in a thread pool
        response = await loop.run_in_executor(None, _sync_search)

        items = response.get("items", [])

        if not items:
            print("[INFO] No search results found.")
            return f"Sir, I couldn't find reliable results for '{query}'."

        print("===== Search Results =====")
        for i, item in enumerate(items, start=1):
            title = item.get("title", "No title")
            snippet = item.get("snippet", "No description")
            link = item.get("link", "No link")

            print(f"\n{i}. {title}")
            print(f"   {snippet}")
            print(f"   Link: {link}")
        print("==========================\n")

        key_points = []
        for item in items[:num_results]:
            title = item.get("title", "")
            snippet = item.get("snippet", "")
            if title and snippet:
                key_points.append(f"{title}. {snippet}")

        summary = (
            f"Sir, I found {len(items)} relevant result{'s' if len(items) > 1 else ''}. "
            f"Here's a concise summary: "
            + " ".join(key_points)
        )

        return summary

    except Exception as e:
        print(f"[ERROR] Google search failed: {e}")
        import traceback
        traceback.print_exc()
        return f"Sir, I'm unable to search for '{query}' at the moment."