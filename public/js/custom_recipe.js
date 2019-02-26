$(function () {
    $('#search_btn').on('click', function() {
        var ingredient_name = $('#ingredient_name').val();
        console.log(ingredient_name);
        if(ingredient_name == '' || ingredient_name.length < 3) {
            return false;
        }
        console.log('button clicked and valid');
        $.ajax({
            url:  "/demo/search-ingredient-ajax/",
            type:  'GET',
            data: { 'ingredient_name':  ingredient_name},
            success: function(data){
                console.log('I am success');
                $("#list_view").html(data);
            }
        });
    })

    $('div#list_view').on('click', 'a.page-link',  function() {
        var ingredient_name = $('#ingredient_name').val();
        var page = $(this).data('page');
        if(ingredient_name == '' || ingredient_name.length < 3) {
            return false;
        }
        console.log(page);
        $.ajax({
            url:  "/demo/search-ingredient-ajax/",
            type:  'GET',
            data: { 'ingredient_name':  ingredient_name, 'page': page },
            success: function(data){
                console.log('I am success');
                $("#list_view").html(data);
            }
        });
    });

    $('div#list_view').on('click', 'a.add_button', function() {
        console.log('This is going to be added in the recipe section');
        var NDB_No = $(this).data('id');
        var qty = $('#qty_'+NDB_No).val();
        var serving_size = $('#serving_'+NDB_No).val();
        var serving_type = $('#serving_'+NDB_No+ ' option:selected').attr('data-serving_type');
        console.log(serving_type);
        $.ajax({
            url:  "/demo/ingredient-detail-ajax/",
            type:  'GET',
            data: { 'NDB_No':  NDB_No, 'qty': qty, 'serving_size': serving_size, 'serving_type' : serving_type },
            success: function(data){
                console.log('I am successful on fetching data');
                $('#recipe_ingredient').append(data)
            }
        });
    })

    $('.recipe-block').on('click', 'a.remove_button', function() {
        $(this).parent().parent().remove();
    })
 
    $('.recipe-block').on('click', 'button#save_recipe', function() {
        var recipe_name = $('#recipe_name').val();
        if(recipe_name == '' || ingredient_name.length < 3) {
            return false;
        }
        var ingredients = [];
        $('tr.ingredient_rows').each(function(index, element) {
            var temp_obj = { 'NDB_No': $(element).attr('data-NDB_No'), 'quantity': $(element).attr('data-quantity'), 'serving_type' : $(element).attr('data-serving_type'), 'serving_size' : $(element).attr('data-serving_size')};
            ingredients.push(temp_obj);
        })
        if(ingredients.length == 0) {
            return false;
        }
        $.post({
            url:  "/customer/save-recipe/",
            type:  'POST',
            dataType: 'json',
            data: { 'recipe_name':  recipe_name, 'ingredients': ingredients},
            success: function(data){
                console.log('Successfully saved recipe');
                alert('Successfully saved recipe')
            }
        });
        console.log('Saving Recipe');

    })

});