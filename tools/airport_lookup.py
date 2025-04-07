from tools.load_airport_data import load_airports
from difflib import get_close_matches
import re
from itertools import combinations

CITY_MAP, CODE_MAP = load_airports()

# Build a map of full airport names to codes (reverse lookup)
NAME_MAP = {name.lower(): code for code, name in CODE_MAP.items()}
KNOWN_CITIES = list(CITY_MAP.keys())
KNOWN_NAMES = list(NAME_MAP.keys())

def fuzzy_match(query, candidates):
    matches = get_close_matches(query.lower(), candidates, n=1, cutoff=0.93)
    return matches[0] if matches else None

def extract_airport_locations(user_input: str) -> list:
    input_lower = user_input.lower()
    seen = set()
    ordered = []

    # Look for IATA codes
    for token in user_input.upper().split():
        if token in CODE_MAP and CODE_MAP[token] not in seen:
            seen.add(CODE_MAP[token])
            ordered.append(CODE_MAP[token])

    # Look for city matches
    for city in CITY_MAP:
        if city in input_lower and city not in seen:
            seen.add(city)
            ordered.append(city)

    return ordered