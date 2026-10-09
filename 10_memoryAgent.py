"""
Memory-enabled tool-calling agent demo.

What this script does:
1. Loads API credentials from `.env`.
2. Creates a chat model.
3. Gives the model access to custom tools from `tools2.py`.
4. Starts a command-line chat loop.
5. Stores previous user, assistant, and tool messages in `conversation_history`.
6. Sends the full message history on every turn so the agent can remember
   earlier parts of the same chat session.

Important:
This memory is temporary. It only lives while this Python script is running.
When the program exits, `conversation_history` is lost. For permanent memory,
you would use a database or a LangGraph checkpointer.
"""

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from tools2 import search_product_catalog, get_daily_menu, calculate_score_percentage

load_dotenv()

# 1. Initialize the chat model.
# Temperature 0 keeps answers more predictable for this learning example.
llm = ChatGoogleGenerativeAI(model="gemini-3.7-flash", temperature=0)
# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 2. Register the tools the agent is allowed to call.
# The model can choose these tools when the user's question needs outside logic.
tools = [search_product_catalog, get_daily_menu, calculate_score_percentage]

# 3. Create the agent.
# `create_agent` builds a LangGraph-backed loop:
# model decides -> tool runs if needed -> model sees tool result -> final answer.
agent = create_agent(model=llm, tools=tools)

# 4. In-memory conversation list that preserves context across turns.
# This is the "memory" in this file.
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
    
    # Add the new user turn to the running conversation.
    conversation_history.append(("user", user_input))
    
    # Send the whole history, not only the latest message.
    # This lets the agent answer follow-up questions using earlier context.
    response = agent.invoke({"messages": conversation_history})
    
    # Save the full updated state.
    # It may include user messages, assistant messages, and tool messages.
    conversation_history = response["messages"]
    
    # The last message is the assistant's final answer for this turn.
    bot_reply = conversation_history[-1].content
    print(f"\nAssistant: {bot_reply}")
