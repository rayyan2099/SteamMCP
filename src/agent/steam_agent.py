import sys
from dotenv import load_dotenv
load_dotenv()

import json
import os

from groq import Groq

from mcp import ClientSession, StdioServerParameters


SYSTEM_PROMPT = """
You are SteamMCP, an intelligent Steam game recommendation assistant.

Understand the user's game preferences and use the available tools.

TOOL RULES:

- If the request contains explicit genres, mechanics, features, or Steam
  tags (for example: metroidvania, RPG, farming, building, management,
  horror, platformer, survival, crafting, simulation, strategy, puzzle,
  open world, action), call recommend_by_preferences.

- If the request contains subjective qualities or vibes (for example:
  dark, relaxing, atmospheric, lonely, cozy, cheerful, strange,
  immersive, mysterious, peaceful, difficult, gloomy), call
  recommend_by_description.

- If the request contains BOTH explicit gameplay preferences and subjective
  descriptions, call BOTH tools.

- If the request only describes a mood or atmosphere without clear gameplay
  preferences, use recommend_by_description.

SPECIFIC GAMES:

- If the user asks for games similar to a specific game, first call
  search_for_games.

- Then call recommend_similar_games using the correct appid.

PLATFORM:

- Platform requirements are hard constraints.
- Always pass the requested platform to recommendation tools.
- Mac or MacBook = mac
- PC or Windows = windows
- Linux = linux

FACTUAL ACCURACY:

- Never invent facts.
- Only use information returned by MCP tools.
- Before giving detailed information about a recommended game, call
  get_game_details_tool.
- Retrieve details for a maximum of 3 games.

FINAL RESPONSE:

- Be concise.
- Recommend the strongest matches first.
- Explain why games fit using tool results only.
- Mention platform compatibility when requested.
"""


def get_groq_tools(mcp_tools):

    groq_tools = []

    for tool in mcp_tools:
        groq_tools.append(
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.input_schema,
                },
            }
        )

    return groq_tools


async def run_agent(
    user_query: str,
    session: ClientSession,
    groq_tools: list
):

    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY")
    )

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_query
        }
    ]

    while True:

        response = client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=messages,
            tools=groq_tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        assistant_message = {
            "role": "assistant",
            "content": message.content
        }

        if message.tool_calls:

            assistant_message["tool_calls"] = [
                {
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments
                    }
                }
                for tool_call in message.tool_calls
            ]

        messages.append(assistant_message)

        # No tools called: final answer
        if not message.tool_calls:
            return message.content

        # Execute tools
        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name

            tool_arguments = json.loads(
                tool_call.function.arguments
            )

            print(f"\nCalling tool: {tool_name}")

            tool_result = await session.call_tool(
                tool_name,
                tool_arguments
            )

            result_content = []

            for content in tool_result.content:

                if hasattr(content, "text"):
                    result_content.append(content.text)

            tool_output = "\n".join(result_content)

            # Keep context small.
            MAX_TOOL_OUTPUT_CHARS = 2000

            if len(tool_output) > MAX_TOOL_OUTPUT_CHARS:
                tool_output = (
                    tool_output[:MAX_TOOL_OUTPUT_CHARS]
                    + "\n[Tool output truncated]"
                )

            # IMPORTANT: Add each tool result ONCE.
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_output
                }
            )


async def create_mcp_connection():
    """
    Create parameters for the persistent MCP server connection.
    """

    return StdioServerParameters(
        command=sys.executable,
        args=["-m", "src.mcp.server"]
    )
