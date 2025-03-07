import json
import logging
from typing import List

from openai import OpenAI

logger = logging.getLogger(__name__)
client = OpenAI()
tool_registry = {}

def has_tool_calls(completion) -> bool:
    return bool(completion.choices[0].message.tool_calls)

def handle_tool_calls(completion) -> List:
    """Handles tool calls from OpenAI completion."""
    tool_responses = [completion.choices[0].message]

    if has_tool_calls(completion):
        for tool_call in completion.choices[0].message.tool_calls:
            try:
                result = tool_registry[tool_call.function.name](
                    **json.loads(tool_call.function.arguments)
                )
                tool_responses.append(
                    {"role": "tool", "tool_call_id": tool_call.id, "content": result}
                )
            except Exception as e:
                logger.exception(
                    f"Failed to call tool: {tool_call.function.name}, Error: {e}"
                )

    return tool_responses

def prompt_model_with_tools_and_text(
    text: str, system_prompt: str, messages: List, model_name: str, tools
):
    """Sends a prompt to OpenAI with optional tools."""
    if not messages:
        messages = [
            {"role": "system", "content": [{"type": "text", "text": system_prompt}]},
            {"role": "user", "content": [{"type": "text", "text": text}]},
        ]

    return client.chat.completions.create(
        model=model_name, messages=messages, tools=tools
    )
