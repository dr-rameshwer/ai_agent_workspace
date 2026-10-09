
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage
from mytools import multiply, get_stock_price

load_dotenv()

# Step 1: Initialize Model
llm = ChatGoogleGenerativeAI(
    model="gemini-3.7-flash",
    temperature=0
)
# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Step 2: Register tools and bind them to the model
tools = [multiply, get_stock_price]
llm_with_tools = llm.bind_tools(tools)

# ADDED: Map tool names to actual Python functions
tool_map = {tool.name: tool for tool in tools}

# Step 3: Ask a question that requires a tool
query = "What is the current stock price of Apple (AAPL)?"
response = llm_with_tools.invoke(query)

print("--- Model Response Payload ---")
print("Content (Text):", response.content)
print("\nTool Calls Requested by Model:")
print(response.tool_calls)

# Store the conversation history
messages = [
    HumanMessage(content=query),
    response
]

# Execute the tools requested by the model
for tool_call in response.tool_calls:
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]
    tool_id = tool_call["id"]

    print(f"\nExecuting '{tool_name}' with {tool_args}")

    # Find and execute the actual Python tool
    result = tool_map[tool_name].invoke(tool_args)
    print("Tool result:", result)

    # Send the tool result back to the model
    messages.append(
        ToolMessage(
            content=str(result),
            tool_call_id=tool_id
        )
    )

# Ask the model to produce a final answer
if response.tool_calls:
    final_response = llm_with_tools.invoke(messages)
    print("\n--- Final Answer ---")
    print(final_response.content)
