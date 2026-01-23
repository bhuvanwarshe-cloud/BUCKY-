# =========================
# Windows asyncio FIX (MUST BE FIRST)
# =========================
import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )

# =========================
# Standard Imports
# =========================
from dotenv import load_dotenv
from livekit import agents
from livekit.agents import (
    AgentSession,
    Agent,
    RoomInputOptions,
    function_tool,
)
from livekit.plugins import google, noise_cancellation

# Imports updated below in usage
from typing import Optional
from pydantic import Field
from datetime import datetime, timezone, timedelta
import os
import httpx


from Bucky_ctrl_windows import (
    livekit_open_app,
    livekit_close_app,
    shutdown_pc,
    restart_pc,
    sleep_pc,
    battery_status,
    livekit_open_folder,
    livekit_close_folder,
    livekit_open_file,
    livekit_close_file,
)

# =========================
# Load environment variables
# =========================
load_dotenv(".env.local")


# =========================
# Assistant Agent (NO realtime init here)
# =========================
class Assistant(Agent):
    pass


# =========================
# LiveKit Entrypoint
# =========================
async def entrypoint(ctx: agents.JobContext):
    # 🔥 Create realtime LLM INSIDE event loop
    llm = google.beta.realtime.RealtimeModel(
        model="gemini-2.5-flash-native-audio-preview-09-2025",
        voice="Charon",
    )

    # Wait for participant to join to get metadata
    participant = await ctx.wait_for_participant()
    
    metadata = participant.metadata
    
    # Generate dynamic prompts
    from BuckyPrompts import get_behavior_prompt, get_greeting_prompt
    behavior_prompt = get_behavior_prompt(metadata)
    greeting_prompt = get_greeting_prompt(metadata)

    agent = Assistant(
        instructions=behavior_prompt,
        llm=llm,
        tools=[
            livekit_open_app,
            livekit_close_app,
            shutdown_pc,
            restart_pc,
            sleep_pc,
            battery_status,
            livekit_open_folder,
            livekit_close_folder,
            livekit_open_file,
            livekit_close_file,
               web_search,
        get_current_datetime,
        get_current_weather,
        system_control,
        ],
    )

    session = AgentSession()

    await session.start(
        room=ctx.room,
        agent=agent,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC()
        ),
    )

    # ⏳ Allow realtime WS + audio pipeline to fully initialize
    await asyncio.sleep(1.5)

    # 🎙️ Scripted greeting (SAFE now)
    await session.generate_reply(
        instructions=greeting_prompt
    )


# =========================
# Tool: Web Search
# =========================
@function_tool(
    name="web_search",
    description="Search Google for up-to-date information."
)
async def web_search(
    query: str = Field(description="Search query"),
) -> str:
    from Bucky_Search import perform_search
    return await perform_search(query, num_results=3)


# =========================
# Tool: Date & Time
# =========================
@function_tool(
    name="get_current_datetime",
    description="Get current date and time in IST."
)
async def get_current_datetime() -> str:
    now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    return now.strftime("%B %d, %Y, %I:%M %p IST")


# =========================
# Tool: Weather (ASYNC SAFE)
# =========================
@function_tool(
    name="get_current_weather",
    description="Get current weather. Defaults to Nagpur, India."
)
async def get_current_weather(
    city: Optional[str] = Field(
        default="Nagpur, India",
        description="City name"
    ),
) -> str:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Sir, my weather system is offline."

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={
                    "q": city,
                    "appid": api_key,
                    "units": "metric",
                },
            )
            data = response.json()

        return (
            f"In {data['name']}, it’s {data['main']['temp']}°C with "
            f"{data['weather'][0]['description']}."
        )
    except Exception:
        return f"Sir, I can’t fetch weather for {city} right now."


# =========================
# Tool: System Control
# =========================
@function_tool(
    name="system_control",
    description="Control Windows system actions."
)
async def system_control(
    action: str = Field(description="Action to perform"),
    params: Optional[str] = Field(default=None),
) -> str:
    from Bucky_ctrl_windows import perform_system_control
    return await perform_system_control(action, params)


# =========================
# Run Worker
# =========================
if __name__ == "__main__":
    agents.cli.run_app(
        agents.WorkerOptions(entrypoint_fnc=entrypoint)
    )
