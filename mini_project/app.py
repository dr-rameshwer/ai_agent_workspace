import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_agent
from schemas import SessionSummary
from tools import technical_search, calculate, save_note

load_dotenv()

# Step A: Initialize Models (Google Gemini or OpenAI GPT)
agent_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
summary_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2).with_structured_output(SessionSummary)

# Step B: Assemble Agent with System Instructions
tools = [technical_search, calculate, save_note]
agent = create_agent(
    model=agent_llm,
    tools=tools,
    system_prompt="You are KnowledgeGenie, an expert AI research assistant. Always use your search and math tools when discussing facts or calculations. Whenever asked to record or save something, use save_note."
)

# Step C: Build the Summary Generator Chain (LCEL)
summary_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert analyst. Based on the conversation history provided, create a structured session summary and concept cards."),
    ("human", "Here is the session log:\n\n{session_log}")
])
summary_chain = summary_prompt | summary_llm

def generate_summary(session_messages):
    """Formats conversation and invokes structured output chain."""
    log_text = ""
    for msg in session_messages:
        role = getattr(msg, "type", "user")
        content = getattr(msg, "content", str(msg))
        if content:
            log_text += f"{role.upper()}: {content}\n"
    
    print("\n⏳ Generating structured summary from your session...")
    summary: SessionSummary = summary_chain.invoke({"session_log": log_text})
    
    print("\n" + "=" * 60)
    print(f"📚 RESEARCH SUMMARY: {summary.subject.upper()}")
    print("=" * 60)
    print("\nKey Takeaways:")
    for point in summary.key_takeaways:
        print(f"  • {point}")
    
    print("\nConcept Cards:")
    for idx, card in enumerate(summary.cards, 1):
        print(f"\n  Card {idx}: [{card.term}]")
        print(f"    Definition: {card.definition}")
        print(f"    Example:    {card.example}")
    print("=" * 60 + "\n")

def main():
    print("=" * 60)
    print("✨ KnowledgeGenie: AI Research & Notes Assistant Active")
    print("Commands:")
    print("  'summary' -> Generate structured concept cards from session")
    print("  'exit'    -> Close the session")
    print("=" * 60)

    messages = []

    while True:
        user_input = input("\nUser: ").strip()
        if not user_input:
            continue
        
        if user_input.lower() == "exit":
            print("👋 Goodbye!")
            break
        
        if user_input.lower() == "summary":
            if not messages:
                print("⚠️ No session history yet to generate summary!")
                continue
            generate_summary(messages)
            continue
        
        # Append message and invoke agent
        messages.append(("user", user_input))
        result = agent.invoke({"messages": messages})
        
        # Keep full message history updated
        messages = result["messages"]
        bot_response = messages[-1].content
        print(f"\nKnowledgeGenie: {bot_response}")

if __name__ == "__main__":
    main()