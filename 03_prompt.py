from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_openai import ChatOpenAI

load_dotenv()

# Step A: Define the prompt blueprint with placeholder variables {language} and {code_snippet}
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are an expert software engineer. Review the given code for performance and readability. Provide 3 bullet points of feedback."),
    ("human", "Here is my {language} code:\n\n{code_snippet}")
])

# Step B: Format the prompt by passing actual values
formatted_messages = prompt_template.invoke({
    "language": "Python",
    "code_snippet": "def add(a, b):\n    return a + b"
})

print("--- Formatted Prompt Messages ---")
print(formatted_messages)