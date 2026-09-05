from dotenv import load_dotenv
load_dotenv()

import json
import os

from groq import Groq
from mcp import Client


SYSTEM_PROMPT = """
You are SteamMCP, an intelligent Steam game recommendation assistant.

Understand the user's request and use the available Steam tools.

TOOL RULES:

- If the user asks for games similar to a specific game:
  first call search_for_games to find the correct Steam appid,
  then call recommend_similar_games.

- If the user gives gameplay preferences, genres, mechanics, or
  recognizable Steam tags such as RPG, metroidvania, farming,
  building, management, horror, platformer, survival, crafting,
  simulation, strategy, puzzle, open world, or action:
  call recommend_by_preferences with the relevant tags.

- Platform requirements are HARD constraints.

- Convert:
  Mac / MacBook → mac
  Windows / PC → windows
  Linux → linux

- Always pass the requested platform to recommendation tools.

- Use get_game_details_tool before giving factual details about
  recommended games.

FACTUAL ACCURACY:

- Never invent facts.
- Only state information returned by MCP tools.
- Do not invent gameplay mechanics, story details, prices,
  playtime, ratings, features, or platform support.

FINAL RESPONSE:

- Recommend the strongest matches first.
- Explain why they fit using tool results.
- Be concise.
"""


def get_groq_tools(mcp_tools):
    """Convert MCP tools into Groq function-calling format."""

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
    client: Client,
    groq_tools: list
):
    """Run the SteamMCP agent using an in-process MCP client."""

    groq_client = Groq(
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

        response = groq_client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=messages,
            tools=groq_tools,
            tool_choice="auto",
            max_tokens=500
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

        # No tool calls means Groq has produced the final answer.
        if not message.tool_calls:
            return message.content

        # Execute requested MCP tools.
        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name

            tool_arguments = json.loads(
                tool_call.function.arguments
            )

            print(
                f"\nCalling tool: {tool_name}",
                flush=True
            )

            tool_result = await client.call_tool(
                tool_name,
                tool_arguments
            )

            result_content = []

            for content in tool_result.content:
                if hasattr(content, "text"):
                    result_content.append(content.text)

            tool_output = "\n".join(result_content)

            # Keep the Groq request small.
            max_tool_output_chars = 2000

            if len(tool_output) > max_tool_output_chars:
                tool_output = (
                    tool_output[:max_tool_output_chars]
                    + "\n[Tool output truncated]"
                )

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_output
                }
            )
