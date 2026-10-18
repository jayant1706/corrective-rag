import json
import re
from typing import Type, TypeVar
from langchain_groq import ChatGroq
from pydantic import BaseModel
from config import GROQ_API_KEY, LLM_MODEL
from utils.logger import logger

T = TypeVar("T", bound=BaseModel)


def get_llm(model: str = None, temperature: float = 0.0) -> ChatGroq:
    """Instantiate a ChatGroq instance with the specified model and temperature."""
    target_model = model or LLM_MODEL
    return ChatGroq(
        model=target_model,
        api_key=GROQ_API_KEY,
        temperature=temperature
    )


def invoke_structured(llm_instance: ChatGroq, prompt, schema_class: Type[T]) -> T:
    """
    Safely invoke the LLM with structured output using json_mode.
    Includes fallback regex JSON parser in case of format variations.
    """
    try:
        structured_llm = llm_instance.with_structured_output(schema_class, method="json_mode")
        result = structured_llm.invoke(prompt)
        if isinstance(result, schema_class):
            return result
        if isinstance(result, dict):
            return schema_class(**result)
    except Exception as e:
        logger.warning(f"Structured output json_mode fallback: {e}")

    # Fallback: Raw invocation with regex JSON extraction
    try:
        raw_res = llm_instance.invoke(prompt)
        text = raw_res.content if hasattr(raw_res, "content") else str(raw_res)
        json_match = re.search(r"\{.*\}", text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group(0))
            return schema_class(**data)
    except Exception as fallback_err:
        logger.error(f"Fallback JSON parsing failed: {fallback_err}")

    # Return default initialized schema instance as fail-safe
    return schema_class()


# Default singleton instance
llm = get_llm()