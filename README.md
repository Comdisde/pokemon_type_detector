# Pokemon Type Detector

![cvmod](https://img.shields.io/static/v1.svg?label=version&message=v1.0&color=green)  ![python](https://img.shields.io/static/v1.svg?label=python&message=3.7&color=blue)

##Overview

**Pokemon Type Detector** es un modelo de deeplearning pre-entrenado que tiene la finalidad de detectar el tipo de pokemon que se le ingrese.
El modelo es una variante del **VGG16** con los pesos de imagenet. 

El output del modelo es el siguiente: 
```python
classes = ['Bug', 'Dark', 'Dragon', 'Electric', 'Fairy', 'Fighting', 'Fire',
           'Flying', 'Ghost', 'Grass', 'Ground', 'Ice', 'No 2nd type', 'Normal',
           'Poison', 'Psychic', 'Rock', 'Steel', 'Water']
```
