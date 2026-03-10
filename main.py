import os
import argparse
from dotenv import load_dotenv

load_dotenv()

from agent import run_agent

def main():

    parser = argparse.ArgumentParser(description="Financial Assistant CLI Agent")

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logs"
    )

    args = parser.parse_args()

    debug_mode = args.debug

    api_key = os.getenv("OPENAI_API_KEY")
    model_name = os.getenv("MODEL_NAME", "gpt-4o-mini")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set in .env")

    print("===================================")
    print(" Financial Assistant CLI Agent ")
    print("===================================")

    if debug_mode:
        print("[DEBUG MODE ENABLED]")

    print("Type 'exit' to quit.\n")

    while True:

        user_input = input("You: ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("Assistant: Goodbye!")
            break

        try:

            response = run_agent(
                user_input=user_input,
                model_name=model_name,
                debug=debug_mode
            )

            print(f"Assistant: {response}\n")

        except Exception as e:
            print(f"Assistant Error: {str(e)}\n")


if __name__ == "__main__":
    main()