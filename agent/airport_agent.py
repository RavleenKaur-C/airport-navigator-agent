import os
import json
from tools.airport_lookup import CITY_MAP, CODE_MAP, extract_airport_locations
from rag.rag_chain import run_rag_chain
from dotenv import load_dotenv
load_dotenv()

CACHE_PATH = "data/airport_cache.json"

if os.path.exists(CACHE_PATH):
    with open(CACHE_PATH) as f:
        airport_cache = json.load(f)
else:
    airport_cache = {}

def chat_with_agent(user_input: str, override_map: dict = None) -> str:
    cities = extract_airport_locations(user_input)
    if not cities:
        return "Sorry, I couldn't figure out your travel cities. Try something like: 'I'm flying from Chicago to Paris to Dubai.'"

    cities = [city.strip().lower() for city in cities if city.strip()]
    cities = list(dict.fromkeys(cities))  # remove duplicates

    response = f"You're traveling through: {', '.join(cities)}\n"

    for city in cities:
        city_key = city.lower()

        if override_map and city_key in override_map:
            airport_name = override_map[city_key]
        elif city_key in CITY_MAP:
            airports = CITY_MAP[city_key]
            if len(airports) == 1:
                airport_name = airports[0]["name"]
            else:
                options = "\n".join([f"• {a['name']}" for a in airports])
                response += f"\nMultiple airports found for **{city.title()}**. Please clarify:\n{options}\n"
                continue
        elif city.upper() in CODE_MAP:
            airport_name = CODE_MAP[city.upper()]
        else:
            response += f"\nNo known airport match for **{city}**."
            continue

        if airport_name in airport_cache:
            rules = airport_cache[airport_name]
        else:
            rules = run_rag_chain(airport_name, "What should I know about airport security and travel tips?")
            if "couldn't find" in rules.lower():
                response += f"\nCouldn’t find info for **{airport_name}**."
                continue
            airport_cache[airport_name] = rules
            with open(CACHE_PATH, "w") as f:
                json.dump(airport_cache, f, indent=2)

        response += f"\n{airport_name}:\n{rules}\n"

    return response.strip()
