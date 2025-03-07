import json
from typing import List
import logging
from openai import OpenAI


client = OpenAI()

tool_names_to_def_dict = {}

logger = logging.getLogger("ToolUtils")

def has_tool_calls(completion)->bool:
    return not completion.choices[0].message.tool_calls is None and len(completion.choices[0].message.tool_calls) >0

def handle_tool_calls(completion)->List:
    tool_response_messages = [completion.choices[0].message]
    if has_tool_calls(completion):
        for tool_call in completion.choices[0].message.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            try:
                result = tool_names_to_def_dict[name](**args)
            except:
                logger.exception(f"Failed to call tool with tool_call {tool_call}")
            tool_response_messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })
    return tool_response_messages

def prompt_model_with_tools_and_text(text:str,system_prompt:str,messages:List,model_name:str,tools):
    if len(messages)==0:
        messages.extend([
                {
                  "role": "system",
                  "content": [
                    {
                      "type": "text",
                      "text": system_prompt
                    }
                  ]
                },
                {
                  "role": "user",
                  "content": [
                    {
                      "type": "text",
                      "text": text
                    }
                  ]
                },
            ]
        )
    return client.chat.completions.create(
        model=model_name,
        messages=messages,
        tools=tools
    )