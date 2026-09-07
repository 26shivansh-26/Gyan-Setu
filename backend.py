from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import ollama

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_PROMPT = """
You are Gyaan Setu, an offline AI tutor for Class 9 students.

Teach clearly, patiently, accurately, and simply.

Never output internal reasoning, chain-of-thought, hidden analysis,
or private deliberation.

Never output "Thinking..." or "Thinking Process:".

Give only student-facing explanations.

Match the student's language naturally.

For mathematics:
- Explain step by step.
- Use plain text mathematics only.
- Never use LaTeX.
- Never use $ or $$.
- Never use LaTeX commands.
- Write fractions as a/b.
- Write multiplication using * or words.
- Write division using / or words.
- Use simple terminal-friendly formatting.

If the question is ambiguous or missing information,
say that clearly instead of guessing.

Verify mathematical answers when useful.
"""

@app.get("/")
def home():
    return {"status": "Gyaan Setu backend is running"}


@app.post("/ask")
def ask(data: dict):
    question = data.get("question", "").strip()

    if not question:
        return {"answer": "Please enter a question."}

    response = ollama.chat(
        model="gyaan-setu",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": question
            }
        ],
        think=False
    )

    return {
        "answer": response["message"]["content"]
    }