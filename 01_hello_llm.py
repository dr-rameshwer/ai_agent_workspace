import os
from dotenv import load_dotenv

# Step A: Load secret keys from .env file into os.environ
load_dotenv()

# Step B: Choose and initialize your model
# Option 1: Google Gemini 3.7 Flash
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(
    model="gemini-3.7-flash",
    temperature=0.7
)

# Option 2: OpenAI GPT-4o-mini (Uncomment if you prefer OpenAI)
# from langchain_openai import ChatOpenAI
# llm = ChatOpenAI(
#     model="gpt-4o-mini",
#     temperature=0.7
# )

# Step C: Send a prompt to the model
prompt_text = "Explain what an API is in one simple sentence for a beginner."
response = llm.invoke(prompt_text)

# Step D: Display the result
print("=" * 60)
print("🤖 AI Model Response:")
print("=" * 60)
print(response.content)