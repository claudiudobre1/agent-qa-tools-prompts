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

## Tema 2: Document Analyst with RAG

### Assignment requirements

Tema 2 asks for a Document Analyst agent using a RAG-style architecture.

The expected functionality includes:

- loading documents
- splitting document text into chunks
- storing documents and chunks
- retrieving relevant chunks based on a user query
- exposing document search as a tool for the agent
- using prompts to guide document-based answers
- allowing the agent to answer questions based on retrieved document context

### What this project implements

This project extends the original QA agent with a local RAG pipeline.

Implemented features:

- `.txt` document loading
- Pydantic models for `Document` and `DocumentChunk`
- paragraph-based text chunking
- local JSON storage for documents and chunks
- simple keyword-based retrieval service
- `search_documents` tool registered through the existing tool registry
- agent integration with document search
- CLI document ingestion using `/ingest`
- dedicated RAG prompt: `rag_answer.yaml`
- debug trace showing the RAG prompt rendering
- automated tests for the document pipeline and RAG search

### RAG module structure

```text
project/documents/
├── __init__.py
├── chunker.py
├── loaders.py
├── models.py
├── rag_service.py
└── repository.py
```

### Document ingestion

Start the CLI:

```bash
python -m project.cli
```

Ingest a document:

```text
You: /ingest data/sample_docs/contract.txt

Ingested document: contract.txt
Document ID: contract
Chunks created: 3
```

### Document search

Ask a document-related question:

```text
You: What does the contract say about termination notice?

Tool used: search_documents
Result: Found 1 relevant chunk(s):

[1] contract.txt | chunk 0
This contract can be terminated with 30 days written notice.
```

### RAG debug mode

The CLI also supports debug mode:

```text
You: /debug What does the contract say about termination notice?
```

This shows the ReAct-style trace, including:

- planner prompt rendering
- selected tool
- retrieved document context
- analyst prompt rendering
- RAG answer prompt rendering

### Current limitations

This is a lightweight local RAG implementation.

Current limitations:

- only `.txt` files are supported
- retrieval is keyword-based, not embedding-based
- storage uses local JSON files, not a vector database
- PDF and DOCX loading are not yet implemented
- final RAG answer generation is rule-based, not LLM-generated

### Future improvements

Possible future improvements:

- add PDF loader
- add DOCX loader
- add embeddings
- add vector search with FAISS, Chroma, or PostgreSQL `pgvector`
- add LLM-based answer generation from retrieved chunks
- add metadata filtering
- add structured document extraction