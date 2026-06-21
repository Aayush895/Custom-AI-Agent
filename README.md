# 🤖 Sir Fix-a-lot (An AI Code Agent)

**`Sir Fix-a-lot` is an autonomous AI agent built in Python that reads, analyzes, and modifies code using Google's Gemini API — all driven by natural language.**

[![Python](https://img.shields.io/badge/Python-3.13%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Gemini API](https://img.shields.io/badge/Gemini-API-4285F4?logo=google&logoColor=white)](https://aistudio.google.com/app/apikey)
[![uv](https://img.shields.io/badge/package%20manager-uv-DE5FE9)](https://docs.astral.sh/uv/)
[![License](https://img.shields.io/badge/license-MIT-green)](#license)

---

## 📖 Overview

AI Code Agent gives an LLM real, bounded agency over a codebase. Instead of just chatting about code, it can:

- Answer questions about how a project works
- Locate and fix bugs on its own
- Execute Python files and read their output
- Iterate — calling tools repeatedly — until it has a complete answer

All of this happens inside a sandboxed directory, with a hard iteration cap to keep things safe and predictable.

> [!WARNING]
> **This agent can read, write, and execute files on your machine.**
> It is sandboxed to the `./calculator` working directory by design, but any AI agent with file-system and code-execution access should be treated as potentially dangerous. Never point it at sensitive directories, and always review what it has done after a run. Do not run this agent in a production environment.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔁 **Iterative agent loop** | The model calls tools repeatedly until it reaches a final answer |
| 📂 **File inspection** | `get_files_info`, `get_file_content` — explore the codebase |
| ✍️ **File writing** | `write_file` — apply fixes and changes directly |
| ▶️ **Python execution** | `run_python_file` — run scripts and read their output |
| 🗣️ **Verbose mode** | Inspect token usage and tool-call details |
| 🛑 **Iteration cap** | `MAX_ITERS` prevents runaway token consumption / infinite loops |

---

## 🧰 Requirements

- Python 3.13+
- [`uv`](https://docs.astral.sh/uv/) — recommended package manager
- A [Google Gemini API key](https://aistudio.google.com/app/apikey)

---

## ⚙️ Setup

**1. Clone the repository**

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

**2. Install dependencies**

```bash
uv sync
```

**3. Configure your API key**

Create a `.env` file in the project root:

```bash
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

> Never commit this file — it's already listed in `.gitignore`.

---

## 🚀 Usage

```bash
uv run main.py "<your prompt here>"
```

### Examples

```bash
# Ask a question about the codebase
uv run main.py "How does the calculator render results to the console?"

# Ask the agent to fix a bug
uv run main.py "There is a bug in the calculator. Find it and fix it."

# Enable verbose output (token counts + tool call results)
uv run main.py "Explain the calculator package structure" --verbose
```

---

## 🔍 How It Works

1. Your prompt is sent to Gemini along with a system prompt and a set of available tools.
2. The model decides which tools to call (e.g. read a file, run a script).
3. Tool results are fed back into the conversation.
4. Steps 2–3 repeat until the model produces a final text response — or the iteration limit is hit.

```
┌─────────┐     ┌────────────┐     ┌──────────────┐
│  Prompt │ ──▶ │   Gemini    │ ──▶ │  Tool Call?   │
└─────────┘     └────────────┘     └──────┬───────┘
                       ▲                  │ yes
                       │                  ▼
                       │           ┌──────────────┐
                       └────────── │ Tool Executes │
                                   └──────────────┘
                                          │ no (final answer)
                                          ▼
                                   ┌──────────────┐
                                   │   Response    │
                                   └──────────────┘
```

---

## 📁 Project Structure

```
.
├── main.py              # Entry point and agent loop
├── call_function.py     # Dispatches tool calls from the model
├── prompts.py           # System prompt definition
├── config.py            # Configuration (e.g. MAX_ITERS)
├── functions/           # Individual tool implementations
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── run_python_file.py
│   └── write_file.py
└── calculator/           # Sandboxed working directory for the agent
    ├── main.py
    └── pkg/
```

---

## ⚠️ Current Limitations
 
- **No persistent conversation / chat history.** Each run of `main.py` is a single, self-contained exchange — you provide one prompt, the agent works through its tool-calling loop, and returns a final answer.
- There is no memory between runs. If you want the agent to act on a follow-up instruction, you'll need to run `main.py` again with a new prompt that includes any context it needs.
- Past conversations are not stored or printed — the agent does not retain or display prior prompts/responses across executions.

---

## 🔒 Safety Notes

- The agent's file access is restricted to the `./calculator` directory.
- A maximum iteration limit (`MAX_ITERS`) prevents infinite loops and excessive API usage.
- All file writes and code executions happen locally — review the `calculator/` directory after any run that modifies files.
- Your Gemini API key is loaded from `.env` and is never hard-coded.

---

## 🛠️ Before You Push — Customize These

- [ ] Replace `<your-username>/<your-repo>` in the clone URL above.
- [ ] If you changed `MAX_ITERS` from the default of `20`, state the new value explicitly.
- [ ] If you extended the agent with extra tools beyond the course, add them to **Features** and **Project Structure**.
- [ ] Add a license file and update the badge/section below if applicable.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<p align="center">Built with 🐍 Python and the Gemini API</p>