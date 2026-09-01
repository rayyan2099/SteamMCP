from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from mcp import Client

from src.mcp.server import mcp
from src.agent.steam_agent import (
    get_groq_tools,
    run_agent,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(">>> Starting SteamMCP", flush=True)

    async with Client(mcp) as client:
        print(">>> MCP client connected", flush=True)

        tools_result = await client.list_tools()

        print(
            f">>> Loaded {len(tools_result.tools)} MCP tools",
            flush=True,
        )

        app.state.mcp_client = client
        app.state.groq_tools = get_groq_tools(tools_result.tools)

        yield

    print(">>> SteamMCP stopped", flush=True)


app = FastAPI(
    title="SteamMCP API",
    description="AI-powered Steam game recommendation API",
    version="1.0.0",
    lifespan=lifespan,
)


class RecommendationRequest(BaseModel):
    query: str


class RecommendationResponse(BaseModel):
    recommendation: str


@app.get("/")
async def root():
    return {
        "message": "SteamMCP API is running"
    }


@app.post(
    "/recommend",
    response_model=RecommendationResponse,
)
async def recommend_games(
    request: RecommendationRequest,
):
    try:
        response = await run_agent(
            user_query=request.query,
            client=app.state.mcp_client,
            groq_tools=app.state.groq_tools,
        )

        return {
            "recommendation": response
        }

    except Exception as error:
        print(f">>> ERROR: {error}", flush=True)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )
