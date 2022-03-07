function copyValueTo(fromElem, toElemId){
    var elem = document.getElementById(toElemId);
    elem.value = fromElem.value;
}

$(document).ready(function(){

    function detailListUpdate(heigth, width, nmb, price_material
        , calc_id, detail_id, is_delete){
        // Ajax обновляет данные в расчёте при изменении количества деталей 
        // и удаляет при тэге is_delete
        var data = {};
        data.calc_id = calc_id;
        data.detail_id = detail_id
        data.heigth = heigth;
        data.width = width;
        data.nmb = nmb;
        data.price_material = price_material;
        data["csrfmiddlewaretoken"] = $('#form-adding-details [name="csrfmiddlewaretoken"]').val();
        if (is_delete){
            data.is_delete = true;
        }
        var form_csrf = $('#form-adding-details');
        var url = form_csrf.attr("action");
        console.log('success')
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: false,
            success: function (data){
                // очищаем форму и сохраняем прошлую цену м2, устанавливаем фокус
                jQuery('#form-adding-details')[0].reset();
                document.getElementById('m2').value = document.getElementById('m2-default').value;
                $('#heigth').focus();
                console.log('success');
                $('.body-table-details-in-calc').html("");
                $.each(data.details, function(key, value){
                        $('.body-table-details-in-calc').append('\
                        <tr>\
                            <td class="col-lg-2">' + value.heigth + '</td>\
                            <td class="col-lg-2">' + value.width + '</td>\
                            <td class="col-lg-2"><input type="number"\
                            class="nmb-detail" data-detail_id="' + value.id + '"\
                            value="' + value.nmb + '"</input></td>\
                            <td class="col-lg-2">' + value.price_material + '</td>\
                            <td class="col-lg-3 table-success text-center">' + value.total_price + '</td>\
                            <td class="delete-item col-lg-1 table-danger text-center" \
                             data-detail_id="' + value.id + '">Удалить&#10006;</td>\
                        </tr>');
                });
                $('#footer-table-details').html("");
                $('#footer-table-details').append('\
                    <th scope="col">Итого корпусная часть:</th>\
                    <th scope="col"></th>\
                    <th scope="col">' + data.details_total_nmb + '</th>\
                    <th scope="col"></th>\
                    <th scope="col" class="text-center">' + data.total_calc_price + '</th>\
                    <th scope="col"></th>\
                ')

            },
            error: function (data){
                console.log('error detail')
            }
        });
    };

    var form = $('#form-adding-details');
    form.on('submit', function(e){
        // Добавляет деталь (Страница: Товар)
        e.preventDefault();
        var heigth = $('#heigth').val();
        var width = $('#width').val();
        var nmb = $('#nmb').val();
        var price_material = $('#m2').val();
        var calc_id = $('#add_detail_to_calc').data("calc_id")
        console.log('form success')
        console.log(heigth,width,nmb,price_material,calc_id)
        detailListUpdate(heigth, width, nmb, price_material, calc_id, 0, is_delete=false)
            
    });
    
    var calc_id = $('#add_detail_to_calc').data("calc_id")
    detailListUpdate(0,0,0,0,calc_id,0,false)
    furnitureListUpdate(0,0,calc_id,false)

    $(document).on('change', '.nmb-detail', function(e){
        e.preventDefault()
        var calc_id = $('#add_detail_to_calc').data("calc_id")
        var detail_id = $(this).data("detail_id")
        var nmb = $(this).val()
        // console.log(calc_id, furniture_id)

        detailListUpdate(0, 0, nmb, 0, calc_id, detail_id, false)
    })

    $(document).on('click', '.delete-item', function(e){
        // Удаляет выбранную по ID деталь из расчёта
        e.preventDefault();
        console.log($(this).data("calc_id"))

        var calc_id = $('#add_detail_to_calc').data("calc_id")
        detailListUpdate(1, 1, 1, 1, calc_id
        ,$(this).data("detail_id"), is_delete=true)

    });

    
    function furnitureListUpdate(furniture_id, nmb, calc_id, is_delete){
        // Ajax обновляет данные в расчёте при изменении количества деталей 
        // и удаляет при тэге is_delete
        var data = {};
        data.calc_id = calc_id;
        data.furniture_id = furniture_id
        data.nmb = nmb;
        data["csrfmiddlewaretoken"] = $('#form-adding-furniture [name="csrfmiddlewaretoken"]').val();
        if (is_delete){
            data.is_delete = true;
        }
        var form_csrf = $('#form-adding-furniture');
        var url = form_csrf.attr("action");
        console.log('success')
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: false,
            success: function (data){
                console.log('success fur');
                $('.form-select-furniture').val(null).trigger('change');
                $('.body-table-furniture-in-calc').html("");
                $.each(data.furniture, function(key, value){
                        $('.body-table-furniture-in-calc').append('\
                        <tr>\
                            <td class="col-lg-5">' + value.title + '</td>\
                            <td class="col-lg-1">' + value.article + '</td>\
                            <td class="col-lg-1">' + value.availability + '</td>\
                            <td class="col-lg-1">' + value.price + '</td>\
                            <td class="col-lg-1"><input type="number"\
                            class="nmb-furniture" data-id="' + value.furniture_id + '"\
                            value="' + value.nmb + '"</input></td>\
                            <td class="col-lg-2 table-success text-center">' + value.total_price + '</td>\
                            <td class="delete-item-furniture col-lg-1 table-danger text-center" \
                             data-id="' + value.id + '">Удалить&#10006;</td>\
                        </tr>');
                });
                $('#footer-table-furniture').html("");
                $('#footer-table-furniture').append('\
                    <th scope="col">Итого:</th>\
                    <th scope="col"></th>\
                    <th scope="col"></th>\
                    <th scope="col"></th>\
                    <th scope="col">' + data.furniture_total_nmb + '</th>\
                    <th scope="col" class="text-center">' + data.total_calc_price + '</th>\
                    <th scope="col"></th>\
                ')

            },
            error: function (data){
                console.log('error detail')
            }
        });
    };


    $(document).on('click', '.delete-item-furniture', function(e){
        // Удаляет выбранную по ID деталь из расчёта
        e.preventDefault();
        var calc_id = $('#add_detail_to_calc').data("calc_id")
        var furniture_id = $(this).data("id")
        console.log(calc_id, furniture_id)
        furnitureListUpdate(furniture_id, 0, calc_id, true)

    });
    

    $('.form-select-furniture').select2({
        width: '100%',
        placeholder: "Выберите фурнитуру",
        language: "ru"
    });
    
    $('.form-select-furniture').change(function(e){
        // alert( "Вызвано событие .dblclick()" );
        e.preventDefault()
        if ($(this).val() !== null){
            var calc_id = $('#add_detail_to_calc').data("calc_id")
            var furniture_id = $('.form-select-furniture option:selected').data("id")
            console.log(calc_id, furniture_id)
            furnitureListUpdate(furniture_id, 1, calc_id, false)
        }    
    });
    $(document).on('change', '.nmb-furniture', function(e){
        e.preventDefault()
        var calc_id = $('#add_detail_to_calc').data("calc_id")
        var furniture_id = $(this).data("id")
        var nmb = $(this).val()
        console.log(calc_id, furniture_id)

        furnitureListUpdate(furniture_id, nmb, calc_id, false)
    })

});