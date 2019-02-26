from django.urls import path

from .views import (
    IngredientSearchOnline,
    IngredientSearch,
    IngredientList,
    IngredientDetail,
    NutrientList,
    WeightList,
    ImportData,
    NutrientDefList,
    RecipeCreationView,
    MealCreationView,

    SearchIngredientAjax,
    IngredientDetailAjax
)

urlpatterns = [
    path('ingredient-search-online/', IngredientSearchOnline.as_view(), name='search-online'),
    path('ingredient-search/', IngredientSearch.as_view(), name='search'),
    path('ingredients/', IngredientList.as_view(), name='ingredient-list'),
    path('ingredients/<str:pk>/', IngredientDetail.as_view(), name='ingredient-detail'),
    path('nutrients/', NutrientList.as_view(), name='nutrient-list'),
    path('weights/', WeightList.as_view(), name='weight-list'),
    path('nutrient-def/', NutrientDefList.as_view(), name='nutrient-def-list'),
    path('import-data/', ImportData.as_view(), name='import-data'),
    path('recipe/', RecipeCreationView.as_view(), name='recipe'),
    path('meal/', MealCreationView.as_view(), name='meal'),

    path('search-ingredient-ajax/', SearchIngredientAjax.as_view(), name='search-ingredient-ajax'),
    path('ingredient-detail-ajax/', IngredientDetailAjax.as_view(), name='ingredient-detail-ajax'),
]
