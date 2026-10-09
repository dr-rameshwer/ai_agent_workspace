from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
# Note: You can also use `from langgraph.prebuilt import create_react_agent as create_agent`
from tools2 import search_product_catalog, get_daily_menu, calculate_score_percentage

load_dotenv()

# 1. Initialize Model & Agent
llm = ChatGoogleGenerativeAI(model="gemini-3.7-flash", temperature=0)
# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

tools = [search_product_catalog, get_daily_menu, calculate_score_percentage]
agent = create_agent(model=llm, tools=tools)

# 2. In-memory conversation list that preserves context across turns
conversation_history = []

print("=" * 60)
print("🤖 Welcome to Operations Assistant CLI (Gemini 3.7 / GPT-4o)")
print("   Type 'exit' to quit")
print("=" * 60)

while True:
    user_input = input("\nYou: ").strip()
    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break
    
    if not user_input:
        continue
    
    # Append the new user turn to history
    conversation_history.append(("user", user_input))
    
    # Invoke the agent with full conversation history
    response = agent.invoke({"messages": conversation_history})
    
    # Update history with full state (including tool executions and assistant answers)
    conversation_history = response["messages"]
    
    # The last message is always the AI's final answer
    bot_reply = conversation_history[-1].content
    print(f"\nAssistant: {bot_reply}")