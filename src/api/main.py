from contextlib import AsyncExitStack, asynccontextmanager
import asyncio

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

    app.state.mcp_session = None
    app.state.groq_tools = None
    app.state.mcp_lock = asyncio.Lock()
    app.state.exit_stack = AsyncExitStack()

    yield

    await app.state.exit_stack.aclose()


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


async def get_mcp_resources():

    if app.state.mcp_session is not None:
        return (
            app.state.mcp_session,
            app.state.groq_tools
        )

    async with app.state.mcp_lock:

        # Check again after acquiring lock
        if app.state.mcp_session is not None:
            return (
                app.state.mcp_session,
                app.state.groq_tools
            )

        server_params = await create_mcp_connection()

        read_stream, write_stream = (
            await app.state.exit_stack.enter_async_context(
                stdio_client(server_params)
            )
        )

        session = await app.state.exit_stack.enter_async_context(
            ClientSession(
                read_stream,
                write_stream
            )
        )

        await session.initialize()

        tools_result = await session.list_tools()

        app.state.mcp_session = session
        app.state.groq_tools = get_groq_tools(
            tools_result.tools
        )

        print(
            "\nSteamMCP server connected successfully."
        )

        return (
            app.state.mcp_session,
            app.state.groq_tools
        )


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

        session, groq_tools = await get_mcp_resources()

        response = await run_agent(
            user_query=request.query,
            session=session,
            groq_tools=groq_tools
        )

        return {
            "recommendation": response
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
