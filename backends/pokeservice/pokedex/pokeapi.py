import requests


from django.conf import settings


def get_pokemon_by_name(name: str):
    """Get a pokémon by name from the pokédex"""
    response = requests.get(f"{settings.POKEAPI_URL}/pokemon/{name}")
    response.raise_for_status()
    return response.json()
