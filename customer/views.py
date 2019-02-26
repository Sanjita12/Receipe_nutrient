from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Recipe, RecipeIngredient, Meal, MealIngredient, RecipeIngredient
from nutrient.models import Ingredient

class RecipeListView(generic.ListView):
    model = Recipe
    paginate_by = 10
    template_name = 'customer/recipe_list.html'

class RecipeDetailView(generic.DetailView):
    model = Recipe
    template_name = 'customer/recipe_detail.html'

    def get_object(self):
        recipe = get_object_or_404(Recipe, pk=self.kwargs['pk'])
        return recipe

    def get_context_data(self, **kwargs):
        context = super(RecipeDetailView, self).get_context_data(**kwargs)
        recipe = self.object
        context['all_ingredients'] = RecipeIngredient.objects.select_related('ingredient').filter(recipe=recipe)
        # major_nutrient_no = ['208', '203', '204', '205', '291', '269']
        # Energy in cal 208,  Protein 203, Total lipid (fat) 204, Carbohydrate 205, fiber 291, Sugars 269,
        # context['major_nutrients'] = Nutrient.objects.select_related('Nutr_No').filter(NDB_No=ingredient).filter(Nutr_No__Nutr_No__in=major_nutrient_no)
        # context['weights'] =  Weight.objects.filter(NDB_No=ingredient)
        return context

class SaveRecipeView(generic.CreateView):
    
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        data = self.request.POST.get('data')
        print(data)
        print(type(data))
        json_data = json.loads(data)
        print(type(json_data))
        if data:
            recipe = Recipe(title=json_data['recipe_name'])
            recipe.save()
            
            ing_obj = None
            for ingredient in json_data['ingredients']:
                print('Inside Loop')
                if ing_obj and ing_obj.NDB_No == ingredient['NDB_No']:
                    pass
                else:
                    try:
                        ing_obj = Ingredient.objects.get(NDB_No=ingredient['NDB_No'])
                    except Ingredient.DoesNotExist:
                        continue
                
                ing = RecipeIngredient(recipe=recipe, ingredient=ing_obj, quantity=ingredient['quantity'], serving_size=ingredient['serving_size'], serving_type=ingredient['serving_type'])
                ing.save()
            return JsonResponse({'id': recipe.id})
        else:
            # empty return error
            return redirect('dashboard')

        # return render(request, 'customer/recipe_detail.html', {})


        # <QueryDict: {'data': ['{"recipe_name":"test","ingredients":[{"NDB_No":"04141","quantity":"1 ","serving_type":"gm","serving_size":"100"},{"NDB_No":"01002","quantity":"1 ","serving_type":"gm","serving_size":"100"}]}'], 'csrfmiddlewaretoken': ['dZtiblJwbvGZMLjggwxaisav2c4RV60XwQXQifjxJj66ju7WUeWelybR137sUVdU']}>