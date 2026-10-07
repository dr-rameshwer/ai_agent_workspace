from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_openai import ChatOpenAI

load_dotenv()

# Step A: Define the desired output schema using Pydantic
class QuizQuestion(BaseModel):
    topic: str = Field(description="The technical topic of the question")
    question: str = Field(description="The multiple-choice question text")
    options: List[str] = Field(description="List of exactly 4 possible answer choices")
    correct_answer_index: int = Field(description="The 0-based index of the correct option (0, 1, 2, or 3)")
    explanation: str = Field(description="A brief explanation of why the correct answer is right")

# Step B: Initialize Model and attach the schema
llm = ChatGoogleGenerativeAI(model="gemini-3.7-flash", temperature=0.2)
# Alternatively: llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

structured_llm = llm.with_structured_output(QuizQuestion)

# Step C: Create the prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert instructor creating technical assessment questions."),
    ("human", "Generate a challenging multiple choice question about {topic} suitable for a {difficulty} level learner.")
])

# Step D: Chain Prompt -> Structured LLM
quiz_chain = prompt | structured_llm

# Step E: Invoke and inspect the typed Python object
quiz_item: QuizQuestion = quiz_chain.invoke({
    "topic": "Python Recursion",
    "difficulty": "Beginner"
})

print("\n--- Generated Quiz Object ---")
print(f"Type: {type(quiz_item)}")
print(f"Topic: {quiz_item.topic}")
print(f"Question: {quiz_item.question}\n")
for idx, opt in enumerate(quiz_item.options):
    marker = "✓" if idx == quiz_item.correct_answer_index else " "
    print(f"  [{idx}] {opt} {marker}")

print(f"\nExplanation: {quiz_item.explanation}")