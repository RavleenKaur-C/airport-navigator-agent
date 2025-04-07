import csv
from collections import defaultdict

def load_airports(path="data/airports.dat"):
    city_map = defaultdict(list)
    code_map = {}

    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            name = row[1]
            city = row[2].lower()
            country = row[3]
            iata = row[4].upper()

            if iata and iata != "\\N":
                airport_data = {"name": name, "code": iata, "country": country}
                city_map[city].append(airport_data)
                code_map[iata] = name

    return dict(city_map), code_map
