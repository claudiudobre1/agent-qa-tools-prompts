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