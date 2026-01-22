# 🦾 BUCKY

**BUCKY** is a real-time, voice-enabled AI assistant built using **LiveKit Agents** and **Google Gemini Realtime**, featuring natural conversations, tool execution, and persistent memory — all wrapped in a modern web interface.

> Talk to your AI assistant in real time.  
> BUCKY listens, understands, remembers, and acts.

---

## ✨ Features

- 🎙️ **Real-time Voice AI**
  - Low-latency speech-to-speech conversations using LiveKit
  - Interruptible responses (barge-in support)

- 🤖 **Gemini Realtime AI**
  - Powered by Google Gemini Realtime models
  - Natural, expressive voice responses

- 🧠 **Persistent Memory**
  - Long-term conversation memory using Mem0
  - Context-aware responses across sessions

- 🛠️ **Tool Calling**
  - Web search (Google Custom Search)
  - Weather lookup
  - Date & time awareness
  - System-level actions (desktop control – local mode)

- 🌐 **Modern Web Interface**
  - Built with Next.js + React
  - Live background video experience
  - One-click “Talk to BUCKY” interaction

- 🔐 **Secure by Design**
  - Environment-based secrets
  - Frontend and backend separated for deployment

---

## 🏗️ Architecture

```text
Frontend (Next.js + LiveKit UI)
        |
        | WebRTC / WebSocket
        ↓
LiveKit Cloud
        |
        ↓
BUCKY Agent (Python)
  - Gemini Realtime
  - Tool execution
  - Memory (Mem0)


#### Environment Variables

You'll also need to configure your LiveKit credentials in `.env.local` (copy `.env.example` if you don't have one):

```env
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
LIVEKIT_URL=https://your-livekit-server-url
```

These are required for the voice agent functionality to work with your LiveKit project.

