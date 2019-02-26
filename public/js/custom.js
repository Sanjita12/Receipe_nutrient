$(function () {
    nutrient_nos = ['208', '204', '203', '205', '291', '269'];
    $('tbody, .main-block').on('change', 'input.qty', function() {
        console.log('Quantity changed');
        var previous = $(this).data('prev');
        var current = this.value;
        console.log('Current: ' + current + ' Previous: '+ previous)
        if(current == 0) {
            $(this).val(previous);
            return false;
        }
        $(this).data('prev', current);
        $(this).attr('value', current);
        $(this).attr('data-prev', current);
        var id = $(this).attr('id');
        console.log(id);
        var row_id = id.split('_')[1]
        $.each(nutrient_nos, function(index,value) {
            var old_val = $('#item_'+row_id+"_"+value).text();
            var new_val = parseFloat(old_val).toFixed(2) * current / previous;
            $('#item_'+row_id+"_"+value).text(new_val.toFixed(3).toString());
        });

    });
    $('tbody, .main-block').on('change', 'select.serving_size', function() {
        console.log('Serving size changed')
        var previous = $(this).data('prev');
        current = this.value;
        console.log('Current: ' + current + ' Previous: '+ previous)
        $(this).data('prev', current);
        $(this).attr('data-prev', current);
        $(this).val(current);
        var id = $(this).attr('id');
        console.log(id);
        var row_id = id.split('_')[1]
        $.each(nutrient_nos, function(index,value) {
            var old_val = $('#item_'+row_id+"_"+value).text();
            var new_val = parseFloat(old_val).toFixed(2) * current / previous;
            $('#item_'+row_id+"_"+value).text(new_val.toFixed(3).toString());
        });
    });
});