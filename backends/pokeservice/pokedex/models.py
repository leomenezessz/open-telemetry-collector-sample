from django.db import models


# Create your models here.


class Pokemon(models.Model):
    name = models.CharField(max_length=100)
    height = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    sprite = models.URLField(default=None, null=True)

    def from_json(self, data):
        self.name = data['name']
        self.height = data['height']
        self.weight = data['weight']
        self.sprite = data['sprites']['front_default']
        return self

    def __str__(self):
        return self.name
