import json
import os
from openai import OpenAI

from tools import get_exchange_rate, get_stock_price
from schemas import TOOLS


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

available_functions = {
    "get_exchange_rate": get_exchange_rate,
    "get_stock_price": get_stock_price
}


messages = [
    {
        "role": "system",
        "content": "You are a helpful financial assistant that can provide stock prices and exchange rates."
    }
]


def run_agent(user_input, model_name, debug=False):

    global messages

    if debug:
        print(f"\n[USER INPUT] {user_input}")

    messages.append({
        "role": "user",
        "content": user_input
    })

    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        tools=TOOLS
    )

    message = response.choices[0].message

    if debug:
        print("\n[LLM RESPONSE RECEIVED]")

    if message.tool_calls:

        if debug:
            print(f"[TOOL CALL COUNT] {len(message.tool_calls)}")

        tool_results = []

        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            if debug:
                print(f"\n[TOOL CALL] {tool_name}")
                print(f"[TOOL ARGS] {tool_args}")

            function_to_call = available_functions.get(tool_name)

            if function_to_call is None:

                result = json.dumps({"error": "Tool not found"})

                if debug:
                    print("[TOOL ERROR] Tool not found")

            else:
                try:
                    result = function_to_call(**tool_args)
                except Exception as e:
                    result = json.dumps({"error": str(e)})

                    if debug:
                        print(f"[TOOL ERROR] {str(e)}")

            if debug:
                print(f"[TOOL RESULT] {result}")

            tool_results.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

        messages.append(message)
        messages.extend(tool_results)

        if debug:
            print("\n[LLM SECOND CALL FOR FINAL ANSWER]")

        second_response = client.chat.completions.create(
            model=model_name,
            messages=messages
        )

        final_message = second_response.choices[0].message.content

        if debug:
            print(f"\n[FINAL ANSWER] {final_message}")

        messages.append({
            "role": "assistant",
            "content": final_message
        })

        return final_message

    else:

        if debug:
            print("\n[NO TOOL NEEDED]")
            print(f"[FINAL ANSWER] {message.content}")

        messages.append(message)

        return message.content