import os
import asyncio
import sys
from dotenv import load_dotenv
from googleapiclient.discovery import build

# Load environment variables
load_dotenv(".env.local")

GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

def safe_print(text: str):
    """
    Safely print text to the console, replacing characters that cannot be encoded.
    This prevents UnicodeEncodeError on Windows terminals with cp1252 encoding.
    """
    try:
        print(text)
    except UnicodeEncodeError:
        # Encode to the stdout encoding (or utf-8 default), replacing errors, then decode back
        encoding = sys.stdout.encoding or 'utf-8'
        safe_text = text.encode(encoding, errors='replace').decode(encoding)
        print(safe_text)

async def perform_search(query: str, num_results: int = 3) -> str:
    """
    Perform Google Custom Search in an async-safe way.
    Designed for LiveKit Agents (non-blocking).
    """

    if not GOOGLE_SEARCH_API_KEY or not SEARCH_ENGINE_ID:
        safe_print("[ERROR] Missing Google Search API key or Search Engine ID")
        return "Sir, my search system is currently offline."

    safe_print("\n===== Google Search Started =====")
    safe_print(f"Query       : {query}")
    safe_print(f"Max results : {num_results}")
    safe_print("================================\n")

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
            safe_print(f"[ERROR] Search execution failed: {e}")
            raise

    try:
        # Run the synchronous search in a thread pool
        response = await loop.run_in_executor(None, _sync_search)

        items = response.get("items", [])

        if not items:
            safe_print("[INFO] No search results found.")
            return f"Sir, I couldn't find reliable results for '{query}'."

        safe_print("===== Search Results =====")
        for i, item in enumerate(items, start=1):
            title = item.get("title", "No title")
            snippet = item.get("snippet", "No description")
            link = item.get("link", "No link")

            safe_print(f"\n{i}. {title}")
            safe_print(f"   {snippet}")
            safe_print(f"   Link: {link}")
        safe_print("==========================\n")

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
        safe_print(f"[ERROR] Google search failed: {e}")
        import traceback
        traceback.print_exc()
        return f"Sir, I'm unable to search for '{query}' at the moment."
