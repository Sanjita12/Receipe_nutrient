from django.db import models

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True, null=True)
    verified =  models.BooleanField(default=False)

class Meal(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True, null=True)
    verified =  models.BooleanField(default=False)
    
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey('nutrient.Ingredient', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)
    serving_size = models.DecimalField(max_digits=5, decimal_places=2)
    serving_type = models.CharField(max_length=84)



class MealRecipe(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='meal_recipes')
    meal = models.ForeignKey('Meal', on_delete=models.CASCADE, related_name='meal_recipes')

class MealIngredient(models.Model):
    meal = models.ForeignKey('Meal', on_delete=models.CASCADE, related_name='meal_ingredients')
    ingredient = models.ForeignKey('nutrient.Ingredient', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)
    serving_size = models.DecimalField(max_digits=5, decimal_places=2)
    serving_type = models.CharField(max_length=84)
