import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

# Load credentials
load_dotenv(".env.local")

GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

async def perform_search(query: str, num_results: int = 3) -> str:
    """
    Perform Google Custom Search using the official Google API client.
    Results are displayed in the terminal and summarized for voice output.
    """
    if not GOOGLE_SEARCH_API_KEY or not SEARCH_ENGINE_ID:
        print("[ERROR] Missing Google Search API key or Search Engine ID in .env.local")
        return "Sir, my search module is offline. Missing Google credentials."

    print(f"\n🔍 ===== Initiating Google Search =====")
    print(f"Query: {query}")
    print(f"Fetching top {num_results} results...\n")

    try:
        service = build("customsearch", "v1", developerKey=GOOGLE_SEARCH_API_KEY)
        response = service.cse().list(q=query, cx=SEARCH_ENGINE_ID, num=num_results).execute()
        items = response.get("items", [])

        if not items:
            print("[INFO] No results found.")
            return f"Sir, I couldn’t find anything for {query}."

        # Print detailed results to terminal
        print("📘 ===== Search Results =====")
        for i, item in enumerate(items, start=1):
            title = item.get("title", "No title")
            snippet = item.get("snippet", "No description")
            link = item.get("link", "No link")
            print(f"\n{i}. {title}\n   {snippet}\n   🔗 {link}")
        print("=============================\n")

        # ✅ New: Combine snippets for more accurate spoken answer
        combined_snippets = " ".join(
            item.get("snippet", "") for item in items[:3] if item.get("snippet")
        )

        if combined_snippets:
            summary = f"Sir, according to Google search, {combined_snippets}"
        else:
            top_titles = [item.get("title", "No title") for item in items[:3]]
            summary = f"Sir, here are the top results for {query}: " + "; ".join(top_titles)

        return summary

    except Exception as e:
        print(f"[ERROR] Search request failed: {e}")
        return f"Sir, I’m unable to search for {query} right now."







