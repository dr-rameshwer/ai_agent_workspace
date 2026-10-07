# LangChain LLM Practice Folder

This folder contains small Python examples for learning how to call chat models with LangChain. The examples start with a simple LLM call, then move into chat messages, prompt templates, pipe chains, and structured output.

## Folder Structure

```text
.
|-- 01_hello_llm.py          # Basic LLM call using invoke()
|-- 02_message.py            # SystemMessage and HumanMessage example
|-- 03_prompt.py             # ChatPromptTemplate example
|-- 04_pipeoperator.py       # Prompt -> model -> parser chain
|-- 05_structureoutput.py    # Pydantic structured output example
|-- .env                     # API keys, never commit this
|-- .gitignore               # Files Git should ignore
|-- requirements.txt         # Python package list
`-- venv/                    # Local virtual environment, ignored by Git
```

Note: this project had a file named `.gitiignore`. The correct Git filename is `.gitignore`.

## Setup

### 1. Create a virtual environment

```bash
python3 -m venv venv
```

### 2. Activate the virtual environment

On macOS or Linux:

```bash
source venv/bin/activate
```

On Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

### 3. Install packages

```bash
python -m pip install -r requirements.txt
```

If you are setting up from scratch without `requirements.txt`, install the main packages manually:

```bash
python -m pip install python-dotenv langchain langchain-core langchain-google-genai langchain-openai pydantic
```

### 4. Create the `.env` file

Create a file named `.env` in the project root.

For Google Gemini:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

For OpenAI, if you switch to `ChatOpenAI`:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Do not share or commit `.env`. It contains private API keys.

## Running the Examples

Make sure the virtual environment is active, then run any file:

```bash
python 01_hello_llm.py
python 02_message.py
python 03_prompt.py
python 04_pipeoperator.py
python 05_structureoutput.py
```

## Requirements File

Generate or update `requirements.txt` after installing packages:

```bash
python -m pip freeze > requirements.txt
```

Install from it on another machine:

```bash
python -m pip install -r requirements.txt
```

For learning projects, a short requirements file with only the packages you directly use is often easier to read than a full `pip freeze` file.

## Git Ignore

The `.gitignore` file should ignore local files that do not belong in Git:

```gitignore
venv/
.env
__pycache__/
*.pyc
.DS_Store
```

Why:

- `venv/` can be recreated from `requirements.txt`.
- `.env` contains private secrets.
- `__pycache__/` and `*.pyc` are generated Python cache files.

## What Each File Does

### `01_hello_llm.py`

This is the simplest model call.

Main ideas:

- `load_dotenv()` loads API keys from `.env`.
- `ChatGoogleGenerativeAI(...)` creates a Gemini chat model object.
- `llm.invoke(prompt_text)` sends one prompt to the model.
- `response.content` prints only the text content from the model response.

### `02_message.py`

This file uses chat-style messages.

Main ideas:

- `SystemMessage` gives the model behavior instructions.
- `HumanMessage` represents the user question.
- `llm.invoke(messages)` sends the full message list to the model.

Use this style when you want clear separation between system instructions and user input.

### `03_prompt.py`

This file creates a reusable prompt template.

Main ideas:

- `ChatPromptTemplate.from_messages(...)` creates a prompt blueprint.
- `{language}` and `{code_snippet}` are placeholders.
- `prompt_template.invoke({...})` fills the placeholders with real values.

This file formats messages but does not call the model.

### `04_pipeoperator.py`

This file builds a full LangChain chain.

Main ideas:

- `prompt | model | parser` connects steps together.
- The prompt creates messages.
- The model generates an AI response.
- `StrOutputParser()` converts the model response into a plain Python string.
- `chain.invoke({...})` runs the whole chain with one input dictionary.

The pipe operator `|` means "send the output of the left step into the right step."

### `05_structureoutput.py`

This file asks the model to return data in a structured Python shape.

Main ideas:

- `BaseModel` creates a Pydantic schema.
- `Field(description=...)` explains each field to the model.
- `List[str]` means a list of strings.
- `llm.with_structured_output(QuizQuestion)` tells LangChain to parse the model output into a `QuizQuestion` object.
- `quiz_chain.invoke({...})` returns a typed object instead of plain text.

Structured output is useful when you want reliable fields like `question`, `options`, `correct_answer_index`, and `explanation`.

## Important Imports

### `load_dotenv`

```python
from dotenv import load_dotenv
```

Loads variables from `.env` into the Python process so libraries can read API keys.

### `ChatGoogleGenerativeAI`

```python
from langchain_google_genai import ChatGoogleGenerativeAI
```

LangChain chat model wrapper for Google Gemini models.

### `ChatOpenAI`

```python
from langchain_openai import ChatOpenAI
```

Optional LangChain chat model wrapper for OpenAI models. It is currently commented out in the examples.

### `SystemMessage` and `HumanMessage`

```python
from langchain_core.messages import SystemMessage, HumanMessage
```

Message classes used to build chat conversations manually.

### `ChatPromptTemplate`

```python
from langchain_core.prompts import ChatPromptTemplate
```

Creates reusable chat prompts with placeholders.

### `StrOutputParser`

```python
from langchain_core.output_parsers import StrOutputParser
```

Converts the model response into a normal string.

### `BaseModel` and `Field`

```python
from pydantic import BaseModel, Field
```

Used to define structured output schemas.

## Important Functions and Concepts

### `invoke()`

`invoke()` runs one LangChain component once.

Examples:

```python
response = llm.invoke("Explain APIs simply")
messages = prompt_template.invoke({"language": "Python"})
result = chain.invoke({"text": "Hello"})
```

What it returns depends on what you invoke:

- Model invoke: usually returns an AI message object.
- Prompt invoke: returns formatted prompt messages.
- Chain invoke: returns the final output of the chain.

### `temperature`

`temperature` controls randomness.

- Low value like `0.2`: more focused and predictable.
- Higher value like `0.7`: more creative and varied.

### Prompt placeholders

Prompt variables are written inside braces:

```python
"Translate the text into {target_tone} style."
```

When invoking, pass matching keys:

```python
chain.invoke({
    "target_tone": "Shakespearean English",
    "text": "I will be late."
})
```

### Pipe operator

The pipe operator builds a chain:

```python
chain = prompt | model | parser
```

This means:

```text
input dictionary -> prompt -> model -> parser -> final result
```

## Switching Between Gemini and OpenAI

For Gemini:

```python
from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(model="gemini-3.7-flash", temperature=0.7)
```

For OpenAI:

```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
```

Also make sure the correct key exists in `.env`.

## Common Issues

### API key error

Check that `.env` exists and contains the correct key:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

Then confirm each file calls:

```python
load_dotenv()
```

### Package not found

Activate the virtual environment and reinstall packages:

```bash
source venv/bin/activate
python -m pip install -r requirements.txt
```

### Model name error

If the provider says the model name does not exist or is unavailable, replace the model string with a currently available model from that provider.

## Suggested Learning Order

1. Run `01_hello_llm.py` to understand a direct model call.
2. Run `02_message.py` to understand system and human messages.
3. Run `03_prompt.py` to understand prompt templates.
4. Run `04_pipeoperator.py` to understand chains.
5. Run `05_structureoutput.py` to understand structured output.
