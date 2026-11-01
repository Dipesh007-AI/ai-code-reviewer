
from langchain_core.prompts import ChatPromptTemplate
from llm import get_llm


assistant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an AI coding assistant.

The user has submitted code for review.

You have access to:
1. The original code
2. The code review
3. The user's question

Your job is to help the user understand and improve their code.

You can:
- Explain bugs
- Explain security issues
- Explain performance problems
- Explain review comments
- Suggest fixes
- Rewrite code
- Improve code
- Explain programming concepts
- Compare original and improved code
- Provide beginner-friendly explanations

Important rules:
- Be accurate and practical.
- Do not invent problems.
- Only discuss issues supported by the provided code or review.
- If unsure, say so.
- Never claim that you executed code unless it was actually executed.
- Explain important changes when providing corrected code.
"""
        ),
        (
            "human",
            """
Original Code:

Language: {language}

Code:
{code}

Code Review:
{review}

User Question:
{question}
"""
        ),
    ]
)


# Create Assistant Chain
def create_assistant_chain():
    llm = get_llm()

    assistant_chain = assistant_prompt | llm

    return assistant_chain
