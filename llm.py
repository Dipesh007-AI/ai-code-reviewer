from langchain_openai import ChatOpenAI

from config import(
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    CHAT_MODEL,
)


def get_llm():
    
    return ChatOpenAI(
        model=CHAT_MODEL,
        api_key =OPENROUTER_API_KEY,
        base_url=OPENROUTER_BASE_URL,
        temperature=0
    )

    