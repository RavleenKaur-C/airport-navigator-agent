import json
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

template = PromptTemplate.from_template("""
You are a helpful airport travel assistant.

Given airport-related text, extract the following fields in JSON:
- tsa_precheck: true/false/null
- liquid_policy: string or null
- customs_info: string or null
- terminal_tips: string or null
- travel_tips: list of 2–5 short bullet-point tips

If any field is missing, return null for it.

Text:
{text}

JSON Output:
""")

def parse_airport_info(text: str) -> dict:
    text = text[:3000]
    response = llm.invoke(template.format(text=text)).content

    try:
        result = json.loads(response)
        if isinstance(result, str):  # double-decoded case
            return json.loads(result)
        return result
    except json.JSONDecodeError:
        print("[!] Warning: invalid JSON returned from LLM")
        return {"raw_response": response}
