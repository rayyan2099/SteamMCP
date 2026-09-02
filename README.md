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
````

---

## 🧠 How It Works

SteamMCP uses an LLM agent to understand the user's request and decide which tools should be used.

For example:

### User Request

> "I want a relaxing farming game."

The AI agent:

1. Understands the user's preferences.
2. Selects the appropriate MCP recommendation tool.
3. Calls the tool through the MCP server.
4. Receives game recommendations.
5. Generates a final response based only on the returned tool results.

---

## 🔌 MCP Tools

The MCP server exposes the following tools.

### `search_for_games`

Search for Steam games by name.

```text
Input:
Game name

Output:
Matching Steam games and app IDs
```

---

### `recommend_similar_games`

Find games similar to a selected Steam game.

```text
Input:
appid
platform (optional)

Output:
Similar games
```

---

### `recommend_by_preferences`

Recommend games based on Steam tags.

Example:

```text
Tags:
farming
crafting
simulation
management
```

Optional platform filtering:

```text
windows
mac
linux
```

---

### `get_game_details_tool`

Retrieve detailed metadata for a Steam game.

Example information includes:

* Game name
* Genres
* Tags
* Platform support
* Ratings
* Price
* Description

---

## 🛠️ Tech Stack

### Backend

* Python
* FastAPI
* Model Context Protocol (MCP)
* Groq
* Pandas
* NumPy

### Frontend

* React
* JavaScript
* CSS

### Deployment

* Render
* Vercel

---

## 📁 Project Structure

```text
SteamMCP/
│
├── src/
│   │
│   ├── agent/
│   │   └── steam_agent.py
│   │
│   ├── api/
│   │   └── main.py
│   │
│   ├── mcp/
│   │   └── server.py
│   │
│   ├── recommenders/
│   │   ├── tag_recommender.py
│   │   └── hybrid_recommender.py
│   │
│   ├── search/
│   │   ├── game_search.py
│   │   └── game_details.py
│   │
│   └── utils/
│       ├── data_loader.py
│       └── filters.py
│
├── data/
│
├── requirements.txt
│
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/rayyan2099/SteamMCP.git
```

```bash
cd SteamMCP
```

---

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it.

#### macOS / Linux

```bash
source venv/bin/activate
```

#### Windows

```bash
venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file:

```text
GROQ_API_KEY=your_groq_api_key_here
```

---

## ▶️ Running the Backend

Start the FastAPI server:

```bash
uvicorn src.api.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

---

## 📚 API Documentation

FastAPI automatically generates interactive API documentation.

Open:

```text
http://localhost:8000/docs
```

---

## 🎮 API Usage

### Recommendation Endpoint

```text
POST /recommend
```

### Request

```json
{
    "query": "I want a relaxing farming game"
}
```

### Response

```json
{
    "recommendation": "Based on your preferences, here are some recommended games..."
}
```

---

## 🤖 Agent Workflow

```text
User Query
    │
    ▼
FastAPI Endpoint
    │
    ▼
SteamMCP Agent
    │
    ▼
Groq LLM
    │
    ▼
Tool Selection
    │
    ▼
MCP Tool Call
    │
    ▼
Steam Recommendation Engine
    │
    ▼
Tool Results
    │
    ▼
LLM Generates Final Recommendation
```

---

## 🧩 Example Queries

### Find Similar Games

```text
Games similar to Stardew Valley
```

### Tag-Based Recommendations

```text
Recommend some open-world survival crafting games
```

### Platform Filtering

```text
Recommend RPG games that work on Mac
```

### Game Search

```text
Find games similar to Hollow Knight
```

---

## 🧠 Recommendation System

SteamMCP uses multiple recommendation strategies.

### Tag-Based Recommendations

Games are compared using Steam tags.

Example:

```text
Input:
farming
crafting
simulation

↓

Find games with similar tags.
```

---

### Similar Game Recommendations

Given a Steam game's `appid`, the system identifies games with similar metadata and tags.

---

### Platform Filtering

Recommendations can be filtered based on platform availability.

Supported platforms:

```text
Windows
macOS
Linux
```

---

## 🔒 Tool-Grounded Responses

The AI agent is instructed to avoid hallucinating game information.

The agent:

* Uses MCP tools to retrieve game data.
* Does not invent game mechanics or metadata.
* Uses retrieved information when generating recommendations.
* Retrieves detailed game information before providing factual details.

---

## 🌐 Deployment

### Backend

The FastAPI backend is deployed using:

**Render**

### Frontend

The React frontend is deployed using:

**Vercel**

---

## 🎯 What I Learned

This project explores several concepts in modern AI engineering:

* AI Agents
* Tool Calling
* Model Context Protocol (MCP)
* LLM Orchestration
* Agent-to-tool communication
* REST API development
* Recommendation systems
* Cloud deployment
* Frontend and backend integration

---

## 🔮 Future Improvements

Potential improvements include:

* [ ] Semantic search using embedding models
* [ ] Improved hybrid recommendation algorithms
* [ ] User accounts and saved recommendations
* [ ] Conversation memory
* [ ] Streaming responses
* [ ] Steam API integration for real-time data
* [ ] Improved frontend UI
* [ ] Recommendation feedback system

---

## 👨‍💻 Author

**Rayyan Kaukab Faridy**

* GitHub: [https://github.com/rayyan2099](https://github.com/rayyan2099)
* LinkedIn: [https://www.linkedin.com/in/rayyan-faridy/](https://www.linkedin.com/in/rayyan-faridy/)

---

## 📄 License

This project is intended for educational and portfolio purposes.

---

⭐ If you found this project interesting, consider giving the repository a star!
