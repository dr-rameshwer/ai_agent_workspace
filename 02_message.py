from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-3.7-flash", temperature=0.2)

messages = [
    SystemMessage(content="You are a senior Linux system administrator. Answer questions in exactly 2 concise sentences."),
    HumanMessage(content="What does the command 'chmod 755' do?")
]

response = llm.invoke(messages)
print("\n--- System Administrator AI Response ---")
print(response.content)