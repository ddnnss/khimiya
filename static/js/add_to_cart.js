function add_to_cart(el) {

        var item_number = document.getElementById('item_total').value
        var item_id = el.dataset.item_id
        var item_name = el.dataset.item_name
     //   var item_price = form.elements["item_price"].value
        var item_image = el.dataset.item_image
     let item_volume = parseFloat(document.getElementsByClassName('select-selected')[0].innerHTML)
     var csrf_token = $('#dummy_form [name="csrfmiddlewaretoken"]').val();

    // console.log($(form).attr('action'));
    //  console.log(csrf_token);
        var data = {};
        data.item_id = item_id;
        data.item_number = item_number;
        data.item_volume = item_volume
        data['csrfmiddlewaretoken'] = csrf_token;
        var url = '/cart/add_to_cart/';
        console.log(data);
        $.ajax({
            url:url,
            type:'POST',
            data: data,
            cache:true,
            success: function (data) {
                console.log('OK');
                // console.log(data.total_items_in_cart);
                // console.log(data.all_items);

                $('.cart_table').empty();
                $('.cart-items').css('display','inline-block')
                $('.cart-items').text(data.total_items_in_cart)

                $.each(data.all_items,function (k,v) {
                  $('.cart_table').append('<tr>\n' +
                     '                            <td>\n' +
                     '                                <img width="40" src="'+ v.image +'" alt="">\n' +
                     '                            </td>\n' +
                     '                            <td>\n' +
                     '                                '+ v.name +' '+v.volume +' л\n' +
                     '                            </td>\n' +
                     '                            <td>\n' +
                     '                                <span id="cart_item_number">'+ v.number+' шт</span> x  <span id="cart_item_price">'+ v.price +' &#8381;</span> = <span id="cart_item_total_price">'+ v.total_price +' &#8381;</span>\n' +
                     '                            </td>\n' +
                     '                        </tr>\n');


                });
                $('.cart_table').append(' <tr class="cart-footer">\n' +
                    '                            <td colspan="2">Итого</td>\n' +
                    '                            <td colspan="2">'+ data.total_cart_price +' &#8381;</td>\n' +
                    '                        </tr>\n' +
                    '                        <tr>\n' +
                    '                            <td colspan="2">\n' +
                    '                                <a href="#" class="btn btn-sm">Открыть корзину</a>\n' +
                    '\n' +
                    '                            </td>\n' +
                    '                            <td colspan="2">\n' +
                    '\n' +
                    '                            <a href="#" class="btn-outline btn-sm">Оплата</a>\n' +
                    '                            </td>\n' +
                    '\n' +
                    '                        </tr>');


            $.amaran({
                        'theme'     :'user blue',
                        'content'   :{
                            img: item_image,
                            user:'Добавлено в корзину:',
                            message: item_number + ' шт. - ' + item_name + ' | ' + item_volume + 'л.'
                        },

                        'position'  :'top right',
                        'outEffect' :'slideRight'
                    });
            },
            error: function () {
                console.log('ERROR')
            }
        })
    }