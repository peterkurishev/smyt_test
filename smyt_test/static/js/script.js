/**
 * Created by Peter A. Kurishev on 10.11.14.
 */

var curModel = null;
var datePickerSettings = null;

function init_date_picker() {
    datePickerSettings = {
        todayBtn: 'linked',
        format: 'yyyy-mm-dd',
        autoclose: true,
        todayHighlight: true
    }
}
function update_object(cell, newValue) {
    var field = (cell.prop('class'));
    var pk = (cell.attr('data-pk'));
    var csrf_token = $('form input[name="csrfmiddlewaretoken"]').val();

    $.ajax({
        url: Urls['smyt:update_record'](curModel),
        type: "POST",
        data: {
            'pk': pk,
            'field': field,
            csrfmiddlewaretoken: csrf_token,
            'value': newValue
        },
        success: function () {
            cell.text(newValue);
        },

        statusCode: {
            400: function () {
                alert('Недопустимое значение');
            }

        },

        error: function () {
            alert("Неизвестная ошибка");
        }
    });
}


function process_edition(cell, oldValue) {
    cell.children().first().focus();

    cell.children().first().keypress(function (e) {
        if (e.which == 13) {
            var newValue = $(this).val();
            if (newValue !== oldValue) {
                update = update_object(cell, newValue);
            } else {
                cell.text(oldValue);
            }
        }
    });
}

function update_table() {
    $('td[editable="true"]').on('click', null, function () {
        if(cell.find("input").length > 0) {
            return;
        }
        var cell = $(this);
        var oldValue = cell.text();
        var dataType = cell.attr('data-type');

        if (dataType == "IntegerField") {
            cell.html('<input type="number" value="' + oldValue + '" />');
            process_edition(cell, oldValue);
        }

        if (dataType == "CharField") {
            cell.html('<input type="text" value="' + oldValue + '" />');
            process_edition(cell, oldValue);
        }

        if (dataType == "DateField") {
            cell.html('<input type="text"  value="' + oldValue + '"/>');
            cell.children().first().datepicker(datePickerSettings).on('hide', function(ev) {
                var newValue = $(this).val();
                if (newValue !== oldValue  && newValue !== undefined) {
                    update = update_object($(this).parent(), newValue);
                } else {
                    $(this).parent().text(oldValue);
                }
            } );
            process_edition(cell, oldValue);
        }
        cell.children().first().focus();
    });
}

function load_data() {
    $.ajax({
        url: Urls['smyt:get_data'](curModel),
        type: "GET",
        success: function (response) {

            // Recreate table
            $('.main > h1').hide();
            $('#result > tbody').empty();
            $('#result > thead').empty().append(response.field_titles.map(function (a) {
                return '<th>' + a + '</th>'
            }).join(''));

            for (var obj in response.objects) {

                $('#result > tbody').append('<tr id="' + response.objects[obj].id + '"></tr>');
                $('#result').find('> tbody > tr#' + response.objects[obj].id).append(response.fields.map(function (a) {
                    var editable = '';
                    if(a!='id')
                        editable = ' editable="true" data-pk="'+response.objects[obj].id+'" class="'+ a +'"';
                    return '<td data-type="' + response.field_types[a] + '"' + editable + '>' + response.objects[obj][a] + '</td>';
                }));
            }
            update_table.call();

        },

        error: function () {
            var message = "Ошибка загрузки данных";
            alert(message);
        }
    });
}
$(document).ready(function () {
    var Initialize = function () {
        init_date_picker();
        $('.model-selector').on('click', null, function (event) {
            event.preventDefault();
            curModel = $(this).attr('model-name');
            load_data.call();
            $.ajax({
                url: Urls['smyt:get_form'](curModel),
                type: "GET",
                success: function (response) {
                    $("#form-wrapper").empty();
                    $("#form-wrapper").append(response);
                    $('form#add_data').on('submit', null, function(event) {
                        event.preventDefault();

                        $.ajax({
                            type: 'POST',
                            url: $(this).prop('action'),
                            data: $(this).serialize(),

                            success: function (response) {
                                load_data.call();
                            },

                            statusCode: {
                                400: function (response) {
                                    $('#form-wrapper').html(response.responseText);
                                    alert("Форма заполнена некорректно");
                                }

                            },

                            error : function (response) {
                                alert("Неизвестная ошибка");
                            }

                        });
                    });

                },

                error: function() { alert("Ошибка загрузки формы"); }
            });
        });


    };

    Initialize();
});