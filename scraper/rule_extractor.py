
import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4", temperature=0)

template = """
You are a helpful travel assistant. Extract the most relevant airport-specific information from the text below.

Format the output as JSON with the following keys:
- tsa_precheck: true/false or null
- liquid_policy: string
- customs_info: string
- terminal_tips: string
- travel_tips: list of 2-5 short tips

If any field is missing, use null.

Text:
{text}

JSON Output:
"""

prompt = PromptTemplate.from_template(template)

def extract_airport_info(text: str) -> str:
    if not text:
        return "{}"
    shortened = text[:3000]  # truncate to avoid token overflow
    return llm.predict(prompt.format(text=shortened))

