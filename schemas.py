from pydantic import BaseModel, Field


class CodeReview(BaseModel):

    score: int = Field(
        description="Overall code quality score from 1 to 10"
    )

    summary: str = Field(
        description="Short summary of the code"
    )

    bugs: list[str] = Field(
        description="Potential bugs or logical problems"
    )

    security: list[str] = Field(
        description="Potential security problems"
    )

    performance: list[str] = Field(
        description="Performance problems or improvements"
    )

    readability: list[str] = Field(
        description="Readability and maintainability issues"
    )

    suggestions: list[str] = Field(
        description="Recommended improvements"
    )