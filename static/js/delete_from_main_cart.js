function delete_from_main_cart(i_id) {
    console.log(i_id);
     jQuery('.cart').showLoading();


    var item_id = i_id;

    var url = '/cart/delete_from_main_cart/';
    var csrf_token = $('#dummy_form [name="csrfmiddlewaretoken"]').val();
    console.log(csrf_token);
      var data = {};
        data.item_id = item_id;
        data['csrfmiddlewaretoken'] = csrf_token;
        console.log(data);
        $.ajax({
            url:url,
            type:'POST',
            data: data,
            cache:true,
            success: function (data){
                $('.cart_table').empty();

                $('.cart-items').text(data.total_items_in_cart)

                if (data.all_items.length > 0) {
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
                      ' <td>\n' +
                      '                            <a class="cart-delete-btn" href="javascript:void(0)"\n' +
                      '                               data-item_id="'+v.id +'"\n' +
                      '                               onclick="delete_from_cart(this)"><span>&#10006;</span></a>\n' +
                      '                        </td>\n'+
                     '                        </tr>\n');


                   });
                      $('.cart_table').append(' <tr class="cart-footer">\n' +
                    '                            <td colspan="2">Итого</td>\n' +
                    '                            <td colspan="2">'+ data.total_cart_price +' &#8381;</td>\n' +
                    '                        </tr>\n' +
                    '                        <tr>\n' +
                    '                            <td colspan="2">\n' +
                    '                                <a href="/cart/" class="btn btn-sm">Открыть корзину</a>\n' +
                    '\n' +
                    '                            </td>\n' +
                    '                            <td colspan="2">\n' +
                    '\n' +
                    '                            <a href="#" class="btn-outline btn-sm">Оплата</a>\n' +
                    '                            </td>\n' +
                    '\n' +
                    '                        </tr>');

                }
                else
                {
                     $('.cart-items').css('display','none')
                     $('.cart_table').append('<tr>\n' +
                         '                          <td> Корзина пуста</td>\n' +
                         '                          </tr>');

                }
            },
            error: function () {
                console.log('ERROR')
            }
        });

}