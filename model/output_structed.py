from typing import Optional

from pydantic import BaseModel, Field

class OutputStructured(BaseModel):
    """
    OutputStructured is a Pydantic model that represents the structured output of a model.
    It contains the following fields:
    - id: An optional string that represents the ID of the output.
    - text: A string that represents the text of the output.
    - score: An optional float that represents the score of the output.
    """
    setup: str = Field(..., description="The setup of the input")
    text: str = Field(..., description="The text of the output")
    