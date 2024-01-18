import os

import requests


POKEMON_EXTERNAL_API_URL = os.environ.get("POKEMON_EXTERNAL_API_URL", "https://pokeapi.co")


def get_pokemon_by_name(name: str):
    """Get a pokémon by name from the pokédex"""
    response = requests.get(f"{POKEMON_EXTERNAL_API_URL}/api/v2/pokemon/{name}")
    response.raise_for_status()
    return response.json()
