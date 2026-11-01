from prompts import review_prompt
from schemas import CodeReview
from llm import get_llm


def create_review_chain():

    # Get the OpenRouter LLM
    llm = get_llm()

    # Tell the LLM to return the CodeReview structure
    structured_llm = llm.with_structured_output(
        CodeReview
    )

    # Create the LangChain Runnable pipeline
    review_chain = (
        review_prompt
        | structured_llm
    )

    return review_chain