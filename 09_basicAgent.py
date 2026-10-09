from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
# Note: You can also use `from langgraph.prebuilt import create_react_agent as create_agent`
from tools2 import search_product_catalog, get_daily_menu, calculate_score_percentage

load_dotenv()

# Step A: Initialize Model (Gemini 3.7 Flash or GPT-4o-mini)
llm = ChatGoogleGenerativeAI(model="gemini-3.7-flash", temperature=0)
# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Step B: Register tools in a list
tools = [search_product_catalog, get_daily_menu, calculate_score_percentage]

# Step C: Create the agent executor
# create_agent builds a compiled state graph containing the LLM node and Tools routing node
agent = create_agent(
    model=llm,
    tools=tools
)

# Step D: Test with a query that requires multi-tool reasoning
query = "What is for lunch on Friday, and is the book 'Python Programming' available in the catalog?"

print(f"User Query: {query}\n")
response = agent.invoke({
    "messages": [("user", query)]
})

# Step E: Inspect the final message
print("--- Final Agent Response ---")
final_message = response["messages"][-1]
print(final_message.content)