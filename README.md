# Financial Assistant CLI Agent

## Overview
This project is a Python CLI financial assistant that uses OpenAI Chat Completions with function calling.
It can answer user questions by calling local tools for:
- stock prices
- exchange rates

The app supports multi-turn chat within a single process session.

## Features
- CLI chat loop with `exit` / `quit` support
- Tool calling for stock price lookup (`get_stock_price`)
- Tool calling for exchange rate lookup (`get_exchange_rate`)
- Optional debug mode (`--debug`) to show tool-call details and intermediate logs

## Project Structure
```text
financial-agent/
├── main.py        # CLI entrypoint and chat loop
├── agent.py       # OpenAI client calls, tool-calling flow, message state
├── tools.py       # Local mock data + tool implementations
├── schemas.py     # Tool schemas passed to the model
├── .gitignore 
└── requirements.txt
```

## Requirements
- Python 3.10+
- An OpenAI API key (`OPENAI_API_KEY`)

Note: This repo currently appears to be run on CPython 3.13 (based on local `__pycache__` artifacts), but the README setup targets Python 3.10+.

## Installation
```bash
# 1) Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# 2) Install dependencies
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your_api_key_here
# Optional (default in code: gpt-4o-mini)
MODEL_NAME=gpt-4o-mini
```

## Run
```bash
# Normal mode
python main.py

# Debug mode
python main.py --debug
```

## Usage Examples
After startup, type prompts directly in the CLI:

```text
You: What is the stock price of AAPL?
Assistant: ...
```

```text
You: What is the exchange rate for USD_TWD?
Assistant: ...
```

Unknown symbol / pair example:

```text
You: What is the stock price of ABCD?
Assistant: ... Data not found ...
```

Exit:

```text
You: exit
Assistant: Goodbye!
```

(`quit` also exits.)

## Example Tasks (A-E)
Use these tasks as a quick demo/acceptance checklist.

1. Task A (Persona)
   - Input: `Who are you?`
   - Expected: The assistant identifies itself as a financial assistant.

2. Task B (Single Tool)
   - Input: `What is the price of NVDA?`
   - Expected: Returns `190.00` (from current mock data).

3. Task C (Parallel Tool Calls in One Turn)
   - Input: `Compare the stock prices of AAPL and TSLA.`
   - Run in debug mode: `python main.py --debug`
   - Expected:
     - Debug log shows multiple tool calls in the same turn (`[TOOL CALL COUNT] 2`).
     - Final answer compares `260.00` vs `430.00`.

4. Task D (Memory Test)
   - Step 1 Input: `My name is [Your Name].`
   - Expected: Agent acknowledges the message.
   - Step 2 Input: `What is my name?`
   - Expected: Agent recalls the name from in-session conversation memory.

5. Task E (Error Handling)
   - Input: `What is the price of GOOG?`
   - Expected: Handles unknown data gracefully (for example, `Data not found`) without crashing.

## How It Works
1. User input is appended to conversation history.
2. First LLM call is made with tool schemas from `schemas.py` (`TOOLS`).
3. If tool calls are returned, local functions in `tools.py` are executed.
4. Tool results are appended to history.
5. Second LLM call generates the final user-facing answer.

## Manual Verification Checklist
1. Fresh start:
   - Follow installation and `.env` setup from this README.
   - Run `python main.py` and confirm startup banner appears.
2. Functional checks:
   - Ask for `AAPL` stock price.
   - Ask for `USD_TWD` exchange rate.
   - Ask for an unknown symbol or pair and confirm graceful error messaging.
3. Debug check:
   - Run `python main.py --debug`.
   - Confirm debug logs show user input, tool calls, tool args, and tool results.
4. Consistency:
   - Confirm command names, file names, and env var names match source code.

## Current Limitations
- Data is mock/static in `tools.py` (not real-time market data).
- Conversation history is in-memory only and resets when the process restarts.
- No automated test suite is currently included in this repo.

## Future Improvements
- Integrate real market/FX APIs
- Add automated tests
- Add persistent conversation memory
