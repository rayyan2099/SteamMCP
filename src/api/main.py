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

    print(">>> API startup complete", flush=True)

    yield

    print(">>> Closing MCP resources", flush=True)

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

    print(">>> Entered get_mcp_resources", flush=True)

    # Reuse existing MCP connection
    if app.state.mcp_session is not None:

        print(">>> Reusing existing MCP session", flush=True)

        return (
            app.state.mcp_session,
            app.state.groq_tools
        )

    print(">>> Waiting for MCP lock", flush=True)

    async with app.state.mcp_lock:

        print(">>> MCP lock acquired", flush=True)

        # Check again after acquiring lock
        if app.state.mcp_session is not None:

            print(
                ">>> MCP session initialized by another request",
                flush=True
            )

            return (
                app.state.mcp_session,
                app.state.groq_tools
            )

        print(">>> Creating MCP parameters", flush=True)

        server_params = await create_mcp_connection()

        print(">>> Starting MCP stdio connection", flush=True)

        read_stream, write_stream = (
            await app.state.exit_stack.enter_async_context(
                stdio_client(server_params)
            )
        )

        print(">>> Stdio connection opened", flush=True)

        print(">>> Creating MCP session", flush=True)

        session = await app.state.exit_stack.enter_async_context(
            ClientSession(
                read_stream,
                write_stream
            )
        )

        print(">>> Initializing MCP session", flush=True)

        await session.initialize()

        print(">>> MCP session initialized", flush=True)

        print(">>> Loading MCP tools", flush=True)

        tools_result = await session.list_tools()

        print(">>> MCP tools loaded", flush=True)

        app.state.mcp_session = session

        app.state.groq_tools = get_groq_tools(
            tools_result.tools
        )

        print(
            ">>> SteamMCP server connected successfully",
            flush=True
        )

        return (
            app.state.mcp_session,
            app.state.groq_tools
        )


@app.get("/")
async def root():

    print(">>> Root endpoint called", flush=True)

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

        print(
            ">>> /recommend request received",
            flush=True
        )

        print(
            ">>> Getting MCP resources",
            flush=True
        )

        session, groq_tools = await get_mcp_resources()

        print(
            ">>> MCP resources ready",
            flush=True
        )

        print(
            ">>> Running agent",
            flush=True
        )

        response = await run_agent(
            user_query=request.query,
            session=session,
            groq_tools=groq_tools
        )

        print(
            ">>> Agent finished",
            flush=True
        )

        return {
            "recommendation": response
        }

    except Exception as error:

        print(
            f">>> ERROR: {error}",
            flush=True
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
