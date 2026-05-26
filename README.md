# Agent QA Tools Prompts

A small Python project that demonstrates a simple QA agent architecture using:

- a tool registry
- Pydantic parameter models
- YAML prompt templates
- a command line interface
- basic pytest coverage

The agent can choose between simple tools such as calculator, datetime, and text statistics.

## Project structure

```text
agent-qa-tools-prompts/
├── project/
│   ├── agent.py
│   ├── cli.py
│   ├── prompts/
│   │   ├── analyst.yaml
│   │   ├── extract.yaml
│   │   ├── planner.yaml
│   │   ├── registry.py
│   │   └── summary.yaml
│   └── tools/
│       ├── basic_tools.py
│       ├── params_models.py
│       ├── registry.py
│       └── tool_wrapper.py
├── tests/
│   └── test_agent.py
├── requirements.txt
└── README.md
```

## Setup

Create a virtual environment:

```bash
python -m venv venv
```

Activate it.

On Windows Git Bash:

```bash
./venv/Scripts/activate
```

On Windows PowerShell:

```powershell
.\venv\Scripts\activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the CLI

```bash
python -m project.cli
```

## CLI examples

### Normal mode

```text
You: 2 * 2

Tool used: calculator
Result: 4
```

### Text statistics example

```text
You: What in God's name do you want now meatbag?

Tool used: text_stats
Result: Characters: 47
Words: 9
Sentences: 1
```

### Datetime example

```text
You: What is the time?

Tool used: datetime
Result: 2026-05-26 13:25:15
```

### Debug mode

Debug mode shows the ReAct-style trace.

```text
You: /debug 25 * 17

REACT TRACE:
Think: Read the user question and inspect available tools.

Act 1: Call tool 'calculator' with arguments {'expression': '25 * 17'}.

Observe 1: 425

FINAL ANSWER:
Tool used: calculator
Result: 425
```

Use debug mode when you want to inspect how the agent selected and called a tool.

## Run tests

```bash
python -m pytest
```

Expected result:

```text
6 passed
```

## Current tools

### calculator

Evaluates simple arithmetic expressions.

Example:

```text
25 * 17
```

Result:

```text
425
```

### datetime

Returns the current local date and time.

Example:

```text
What is the time?
```

### text_stats

Counts characters, words, and sentences.

Example:

```text
What in God's name do you want now meatbag?
```

## Development workflow

Check status:

```bash
git status
```

Run tests:

```bash
python -m pytest
```

Commit changes:

```bash
git add .
git commit -m "Describe the change"
git push
```