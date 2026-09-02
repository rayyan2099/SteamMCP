# 🎮 SteamMCP

### AI-Powered Steam Game Recommendation Agent

SteamMCP is an agentic AI application that recommends Steam games based on natural language preferences. It uses the **Model Context Protocol (MCP)** to allow an LLM agent to dynamically discover and invoke specialized recommendation tools.

The application supports game search, similarity-based recommendations, tag-based recommendations, platform filtering, and detailed game metadata retrieval.

🌐 **Live Demo:** https://steam-mcp-alpha.vercel.app/

---

## 🚀 Features

- 🤖 AI-powered game recommendations using an LLM agent
- 🔌 Model Context Protocol (MCP) tool integration
- 🔍 Search Steam games by name
- 🎮 Find games similar to a selected game
- 🏷️ Recommend games based on Steam tags and preferences
- 💻 Filter recommendations by platform
  - Windows
  - macOS
  - Linux
- 📖 Retrieve detailed game information
- 🌐 REST API built with FastAPI
- ⚛️ React frontend
- ☁️ Cloud deployment using Render and Vercel

---

## 🏗️ Architecture

```text
                    User
                     │
                     ▼
              React Frontend
                     │
                     ▼
                FastAPI API
                     │
                     ▼
                AI Agent
                     │
                     ▼
              Groq LLM API
                     │
              Tool Selection
                     │
                     ▼
              MCP Client / Server
                     │
       ┌─────────────┼─────────────┐
       ▼             ▼             ▼
 Game Search    Tag Recommender  Game Details
       │             │             │
       └─────────────┼─────────────┘
                     │
                     ▼
                Steam Dataset
