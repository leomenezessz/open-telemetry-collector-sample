import logging

from django.shortcuts import render
from django.views import View
from requests import RequestException, HTTPError
from .forms import PokemonForm
from .models import Pokemon
from .pokeapi import get_pokemon_by_name

logger = logging.getLogger("pokeservice")


class PokemonView(View):
    from_class = PokemonForm
    template_name = 'search_pokemon.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.from_class()})

    def post(self, request, *args, **kwargs):
        form = self.from_class(request.POST)
        pokemon = None

        try:
            if form.is_valid():

                name = form.cleaned_data['name']

                logger.info(f"Searching pokémon: {name}")

                pokemon = Pokemon.objects.filter(name=name).first()

                if not pokemon:
                    data = get_pokemon_by_name(name)
                    pokemon = Pokemon().from_json(data)
                    pokemon.save()

            logger.info(f"Pokemon found: {pokemon.name}",
                        extra={"_name": pokemon.name, "_height": f"{pokemon.height}", "_weight": f"{pokemon.weight}"})

            return render(request, self.template_name, {'form': self.from_class(), 'pokemon': pokemon})

        except (RequestException, HTTPError, Exception) as e:
            form.add_error('name', 'Pokemon not found.')
            logger.exception(f"Pokemon not found: {e}", exc_info=True)
            return render(request, self.template_name, {'form': form})
