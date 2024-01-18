from django.forms import ModelForm
from .models import Pokemon


class PokemonForm(ModelForm):
    class Meta:
        model = Pokemon
        fields = ['name']
        labels = {
            'name': 'Pokemon name'
        }
        help_texts = {
            'name': 'Enter a pokemon name'
        }
        error_messages = {
            'name': {
                'max_length': 'Pokemon name is too long'
            }
        }
