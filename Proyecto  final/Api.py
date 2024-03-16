import requests

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/pokemon/"


def get_pokemon_info(pokemon_name):
    url = f"{POKEAPI_BASE_URL}{pokemon_name.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
