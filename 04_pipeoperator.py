from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
# Or: from langchain_openai import ChatOpenAI

load_dotenv()

# 1. Define Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a witty translator. Translate the text into {target_tone} style."),
    ("human", "{text}")
])

# 2. Define Model (Gemini 3.7 or GPT-4o-mini)
model = ChatGoogleGenerativeAI(model="gemini-3.7-flash", temperature=0.7)
# model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# 3. Define Output Parser
parser = StrOutputParser()

# 4. Compose the Chain using the pipe operator (|)
chain = prompt | model | parser

# 5. Execute the Chain with a single input dictionary
result = chain.invoke({
    "target_tone": "Shakespearean Elizabethan English",
    "text": "Hey bro, I will be late for the meeting because traffic is terrible."
})

print("--- Translated Output ---")
print(result)