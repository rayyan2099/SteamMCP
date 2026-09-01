from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from mcp import ClientSession
from mcp.client.stdio import stdio_client

from src.agent.steam_agent import (
    create_mcp_connection,
    get_groq_tools,
    run_agent
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    server_params = await create_mcp_connection()

    async with stdio_client(
        server_params
    ) as (read_stream, write_stream):

        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            await session.initialize()

            tools_result = await session.list_tools()

            app.state.mcp_session = session
            app.state.groq_tools = get_groq_tools(
                tools_result.tools
            )

            print("\nSteamMCP server connected successfully.")

            yield

    print("\nSteamMCP server disconnected.")


app = FastAPI(
    title="SteamMCP API",
    description="AI-powered Steam game recommendation API",
    version="1.0.0",
    lifespan=lifespan
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
    response_model=RecommendationResponse
)
async def recommend_games(
    request: RecommendationRequest
):
    try:

        response = await run_agent(
            user_query=request.query,
            session=app.state.mcp_session,
            groq_tools=app.state.groq_tools
        )

        return {
            "recommendation": response
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )