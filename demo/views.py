from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.http import Http404
from django.views import generic
from django.conf import settings
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Prefetch
from django.forms.models import model_to_dict
from decimal import Decimal

import requests
import os
import time
import math

from nutrient.models import Ingredient, Nutrient, Weight, NutrientDef

class IngredientSearchOnline(generic.TemplateView):
    
    template_name = 'demo/ingredient_search_online.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # self.load_data()
        ingredient_name = self.request.GET.get('ingredient_name')

        if ingredient_name:
            url = "https://api.nal.usda.gov/ndb/search/?format=json&q="+ingredient_name+"&sort=n&max=25&offset=0&api_key=DEMO_KEY"
            response = requests.get(url)
            context['items'] = response.json()
        else: 
            context['items'] = []
        return context

class IngredientSearch(generic.ListView):
    
    template_name = 'demo/ingredient_search.html'
    paginate_by = 25
    context_object_name = "results"

    def get_queryset(self):
        ingredient_name = self.request.GET.get('ingredient_name')
        if ingredient_name:
            major_nutrient_no = ['208', '203', '204', '205', '291', '269']
            return Ingredient.objects.prefetch_related('weights', 
                Prefetch('nutrients', queryset=Nutrient.small_reports.all(), to_attr='major_nutrients')
            ).annotate(
                search=SearchVector('NDB_No', 'Shrt_Desc', 'Long_Desc', 'ComName')
            ).filter(search=ingredient_name).all()

        else:
            return []

class RecipeCreationView(generic.TemplateView):
    template_name = 'demo/recipe.html'
    paginate_by = 15

class MealCreationView(generic.TemplateView):
    template_name = 'demo/meal.html'
    paginate_by = 15

class IngredientList(generic.ListView):
    template_name = 'demo/ingredients.html'
    model = Ingredient
    paginate_by = 100

class IngredientDetailAjax(generic.ListView):
    context_object_name = 'ingredient'
    model = Ingredient

    def get(self, request):
        if self.request.is_ajax():
            pk = self.request.GET.get('NDB_No')
            qty = Decimal(self.request.GET.get('qty', 1))
            serving_size = Decimal(self.request.GET.get('serving_size', 100))
            serving_type= self.request.GET.get('serving_type', '100gm')
            try:
                ingredient =  Ingredient.objects.prefetch_related('weights', 
                    Prefetch('nutrients', queryset=Nutrient.small_reports.all(), to_attr='major_nutrients')
                ).get(NDB_No=pk)
                nutrients = ingredient.major_nutrients
                nutrients_dict = {'208': None, '204' : None, '203' : None, '205': None, '291': None, '269': None}
                for nutrient in nutrients:
                    nutrients_dict[nutrient.Nutr_No.Nutr_No] = qty * serving_size * nutrient.Nutr_Val / 100
                print(nutrients_dict)
            except Ingredient.DoesNotExist:
                ingredient = {}
            return render(request, "demo/recipe_ingredient.html", {'ingredient':  ingredient , 'qty': qty, 'serving_size': serving_size, 'nutrients': nutrients_dict, 'serving_type': serving_type})
        
    

class SearchIngredientAjax(generic.ListView):
    context_object_name = 'ingredients'
    model = Ingredient
    template_name = 'demo/recipe.html'
    paginate_by = 10

    def make_pagination_html(self, current_page, total_pages):
        pagination_string = ""
        pagination_string += '<ul class="pagination" style="justify-content: center;">'
        
        if current_page == 1:
            pagination_string += '<li class="page-item disabled"> \
                <a class="page-link" href="#" tabindex="-1" aria-label="Previous">'
        else:
            pagination_string += '<li class="page-item"> \
                <a class="page-link" href="javascript:void(0)" data-page="%s" aria-label="Previous">' %(current_page - 1)
        pagination_string += '<span aria-hidden="true">&laquo;</span>\
                    <span class="sr-only">Previous</span>\
                </a>\
            </li>'
        
        for num in range(1, total_pages):
            if num == current_page:
                pagination_string += '<li class="page-item active">\
                    <a class="page-link" href="#" data-page="%s">%s<span class="sr-only">(current)</span></a>\
                </li>' %(num, num)
            else:
                pagination_string += '<li class="page-item">'
                if num-3 <= current_page and current_page <= num+3:
                    pagination_string += '<a class="page-link" href="javascript:void(0)" data-page="%s">%s</a>' %(num, num)
                elif num%10 == 0 or num == total_pages:
                    pagination_string += '<a class="page-link" href="javascript:void(0)" data-page="%s">%s</a>' %(num, num)
                    
        if current_page == total_pages:
            pagination_string += '<li class="page-item disabled"> \
                <a class="page-link" href="#" tabindex="-1" aria-label="Next">'
        else:
            pagination_string += '<li class="page-item"> \
                <a class="page-link" href="javascript:void(0)" data-page="%s" aria-label="Previous">' %(current_page + 1)
        pagination_string += '<span aria-hidden="true">&raquo;</span>\
                    <span class="sr-only">Next</span>\
                </a>\
            </li>'
        pagination_string += '</ul>'
        return pagination_string

    def get_queryset(self):
        ingredient_name = self.request.GET.get('ingredient_name')
        if ingredient_name:
            major_nutrient_no = ['208', '203', '204', '205', '291', '269']
            return Ingredient.objects.prefetch_related('weights', 
                Prefetch('nutrients', queryset=Nutrient.small_reports.all(), to_attr='major_nutrients')
            ).annotate(
                search=SearchVector('NDB_No', 'Shrt_Desc', 'Long_Desc', 'ComName')
            ).filter(search=ingredient_name)

        else:
            return []

    def get(self, request):
        if self.request.is_ajax():
            current_page = int(self.request.GET.get('page', 1))
            print(current_page)
            limit = self.paginate_by * current_page
            offset = limit - self.paginate_by
            ingredients = self.get_queryset()[offset:limit]
            total_ingredients = self.get_queryset().count()
            total_pages = total_ingredients / self.paginate_by
            total_pages = math.ceil(total_pages)
            pagination = self.make_pagination_html(current_page, total_pages)
            
            return render(request, "demo/search_ingredients.html", {'ingredients':  ingredients, 'pagination': pagination})
        else:
            return render(request, "demo/recipe.html", {'ingredients':  []})

class IngredientDetail(generic.DetailView):
    template_name = 'demo/ingredient_detail.html'
    model = Ingredient
    context_object_name = 'ingredient'
    
    def get_object(self):
        ingredient = get_object_or_404(Ingredient, NDB_No=self.kwargs['pk'])
        return ingredient

    def get_context_data(self, **kwargs):
        context = super(IngredientDetail, self).get_context_data(**kwargs)
        ingredient = self.object
        context['all_nutrients'] = Nutrient.objects.select_related('Nutr_No').filter(NDB_No=ingredient).exclude(Nutr_Val=0)
        major_nutrient_no = ['208', '203', '204', '205', '291', '269']
        # Energy in cal 208,  Protein 203, Total lipid (fat) 204, Carbohydrate 205, fiber 291, Sugars 269,
        context['major_nutrients'] = Nutrient.objects.select_related('Nutr_No').filter(NDB_No=ingredient).filter(Nutr_No__Nutr_No__in=major_nutrient_no)
        context['weights'] =  Weight.objects.filter(NDB_No=ingredient)
        return context
        

class NutrientList(generic.ListView):
    template_name = 'demo/nutrients.html'
    model = Nutrient
    paginate_by = 1000

class WeightList(generic.ListView):
    template_name = 'demo/weights.html'
    model = Weight
    paginate_by = 100

class NutrientDefList(generic.ListView):
    template_name = 'demo/nutrient_def.html'
    model = NutrientDef
    paginate_by = 20

class ImportData(generic.TemplateView):
    template_name = 'demo/import.html'
    
    def load_data(self):
        def change_field_val(str):
            if str.startswith('~') and str.endswith('~') and len(str) == 2:
                return ''
            elif str.startswith('~') and str.endswith('~'):
                return str[1:-1]
            elif not str:
                return None
            else:
                return float(str)
        parse_start = time.time()

        product_obj_keys = [
            'NDB_No',
            'FdGrp_Cd',
            'Long_Desc',
            'Shrt_Desc',
            'ComName',
            'ManufacName',
            'Survey',
            'Ref_desc',
            'Refuse',
            'SciName',
            'N_Factor',
            'Pro_Factor',
            'Fat_Factor',
            'CHO_Factor'
        ]
        weight_obj_keys = [
            'NDB_No',
            'Seq',
            'Amount',
            'Msre_Desc',
            'Gm_Wgt',
            'Num_Data_Pts',
            'Std_Dev'
        ]
        nutrient_obj_keys = [
            'NDB_No',
            'Nutr_No',
            'Nutr_Val',
            'Num_Data_Pts',
            'Std_Error',
            'Src_Cd',
            'Deriv_Cd',
            'Ref_NDB_No',
            'Add_Nutr_Mark',
            'Num_Studies',
            'Min',
            'Max',
            'DF',
            'Low_EB',
            'Up_EB',
            'Stat_cmt',
            'AddMod_Date'
        ]
        nutrient_def_obj_keys = [
            'Nutr_No',
            'Units',
            'Tagname',
            'NutrDesc',
            'Num_Dec',
            'SR_Order'
        ]


        dictfilt = lambda x, y: dict([ (i,x[i]) for i in x if i in set(y) ])
        weight_obj_model_keys = ('NDB_No', 'Seq', 'Amount', 'Msre_Desc', 'Gm_Wgt', 'Std_Dev')
        nutrient_obj_model_keys = ('Nutr_No', 'NDB_No', 'Nutr_Val', 'Std_Error', 'Deriv_Cd', 'Ref_NDB_No', 'Add_Nutr_Mark')
        nutrient_def_obj_model_keys = ('Nutr_No', 'Units', 'Tagname', 'NutrDesc', 'Num_Dec', 'SR_Order')

        parsed_data = {}
        filepath_list = {'ingredient': 'FOOD_DES.txt', 'nutrient': 'NUT_DATA.txt', 'weight': 'WEIGHT.txt', 'nut_def': 'NUT_DEF.txt'}
        key_list = {'ingredient': product_obj_keys, 'nutrient': nutrient_obj_keys, 'weight': weight_obj_keys, 'nut_def': nutrient_def_obj_model_keys}
        for key,filepath in filepath_list.items():
            with open(os.path.join(settings.BASE_DIR, filepath), 'r') as file_object:
                line = file_object.readline()
                parsed_data[key] = []
                while line:
                    fields = line.strip().split('^')
                    if len(fields) != len(key_list[key]):
                        print('Unequal fields hence invalid')
                    for idx,item in enumerate(fields):
                        parsed_str = change_field_val(item)
                        fields[idx] = parsed_str
                    line = file_object.readline()
                    parsed_data[key].append(dict(zip(key_list[key], fields)))
        parse_end = time.time()
        print('Parsed in ' + str(parse_end-parse_start))
        print('Data is now parsed')
        for key, data in parsed_data.items():
            if key == 'ingredient':
                pass
                # for ingredient in data:
                #     Ingredient(**ingredient).save()
            elif key == 'weight':
                pass
                # print('Inside Weight')
                # ingredient_obj = None
                # for weight in data:
                #     start_create = time.time()
                #     weight = dictfilt(weight, weight_obj_model_keys)
                #     # to refer ingredient we need to fetch it
                #     if ingredient_obj and ingredient_obj.NDB_No == weight['NDB_No']:
                #         weight['NDB_No'] = ingredient_obj
                #     else:
                #         ingredient_obj = Ingredient.objects.get(NDB_No=weight['NDB_No'])
                #         weight['NDB_No'] = ingredient_obj
                #     try:
                #         Weight(**weight).save()
                #     except:
                #         print('Already in the system')
                #     end_create = time.time()
                #     print('Created in ' + str(end_create-start_create))
            elif key == 'nutrient':
                pass
                # to refer ingredient, nutrient def we need to fetch it
                print('Inside Nutrient')
                ingredient_obj = None
                nutrient_def_obj = None
                for nutrient in data:
                    start_create = time.time()
                    nutrient = dictfilt(nutrient, nutrient_obj_model_keys)
                    print(ingredient_obj)
                    if ingredient_obj and ingredient_obj.NDB_No == nutrient['NDB_No']:
                        print('Already fetched ingredient')
                        nutrient['NDB_No'] = ingredient_obj
                    else:
                        print('Not fetched. Fetching ingredient now')
                        ingredient_obj = Ingredient.objects.get(NDB_No=nutrient['NDB_No'])
                        nutrient['NDB_No'] = ingredient_obj
                    if nutrient_def_obj and nutrient_def_obj.Nutr_No == nutrient['Nutr_No']:
                        print('Already fetched nutrient_def')
                        nutrient['Nutr_No'] = nutrient_def_obj
                    else:
                        print('Not fetched. Fetching nutrient_def now')
                        nutrient_def_obj = NutrientDef.objects.get(Nutr_No=nutrient['Nutr_No'])
                        nutrient['Nutr_No'] = nutrient_def_obj
                    try:
                        Nutrient(**nutrient).save()
                    except:
                        print('Already in the system')
                    end_create = time.time()
                    print('Created in ' + str(end_create-start_create))
            elif key == 'nut_def':
                pass
                # print('Inside Nut Def')
                # start_create = time.time()

                # for nut_def in data:
                #     NutrientDef(**nut_def).save()
                # end_create = time.time()
                # print('Created in ' + str(end_create-start_create))
    def clear_data(self):
        pass
        # Nutrient.objects.all().delete()
        # Weight.objects.all().delete()
        # Ingredient.objects.all().delete()
        # NutrientDef.objects.all().delete()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # self.clear_data()
        # self.load_data()
        count_obj_list = { 'ingredient': 0, 'nutrient': 0, 'weight': 0, 'nutrient_def': 0 }
        count_obj_list['ingredient'] = Ingredient.objects.all().count()
        count_obj_list['nutrient'] = Nutrient.objects.all().count()
        count_obj_list['weight'] = Weight.objects.all().count()
        count_obj_list['nutrient_def'] = NutrientDef.objects.all().count()
        context['count_obj_list'] = count_obj_list
        return context