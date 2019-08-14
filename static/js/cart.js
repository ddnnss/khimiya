function change_cart(obj) {
    jQuery('.cart').showLoading();
    var item_id = $(obj).data('item_in_cart_id');
    var item_number = $(obj).val();
    if (parseInt(item_number) > 0){
        var url = '/cart/update_cart/';
        var csrf_token = $('#dummy_form [name="csrfmiddlewaretoken"]').val();
        var data = {};
        data.item_id = item_id;
        data.item_number = item_number;
        data['csrfmiddlewaretoken'] = csrf_token;
        console.log(data);
        $.ajax({
            url:url,
            type:'POST',
            data: data,
            cache:true,
            success: function (data) {
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
                      $('#cart_body').empty()
                      $.each(data.all_items,function (k,v) {
                          $('#cart_body').append(' <tr class="main-cart-item">\n' +
                              '                    <td>\n' +
                              '                        <div class="main-cart-item-name">\n' +
                              '                            <img src="'+ v.image +'" alt=""> <span>'+ v.name +' '+ v.volume +' л</span>\n' +
                              '                        </div>\n' +
                              '\n' +
                              '                    </td>\n' +
                              '                    <td class="main-cart-item-number">\n' +
                              '                        <div class="custom-input main-cart">\n' +
                              '                            <button class="custom-input-minus" data-item_id="'+ v.id +'" onclick="mainCartMinusItem(this)">-</button>\n' +
                              '                            <input id="'+ v.id +'_item_total" data-item_in_cart_id="'+ v.id +'" value="'+ v.number +'" disabled onchange="change_cart(this)">\n' +
                              '                            <button class="custom-input-plus" data-item_id="'+ v.id +'" onclick="mainCartPlusItem(this)">+</button>\n' +
                              '\n' +
                              '                        </div>\n' +
                              '                    </td>\n' +
                              '                    <td class="main-cart-item-price">'+ numberWithCommas(v.price) +' &#8381;</td>\n' +
                              '                    <td class="main-cart-item-total-price">'+ numberWithCommas(v.total_price) +' &#8381;</td>\n' +
                              '                    <td class="main-cart-item-action"><a class="cart-delete-btn" onclick="delete_from_main_cart('+ v.id +')" href="javascript:void(0)"><span>&#10006;</span></a></td>\n' +
                              '                </tr>')
                      });
                     $('#cart_body').append(' <tr class="main-cart-footer">\n' +
                            '                    <td class="main-cart-footer__total">Итого</td>\n' +
                            '                    <td></td>\n' +
                            '                    <td></td>\n' +
                            '                    <td colspan="2" class="main-cart-footer__total-price">'+ numberWithCommas(data.total_cart_price)+' &#8381;</td>\n' +
                            '\n' +
                            '                </tr>')
                jQuery('.cart').hideLoading()
                }
            },
            error: function () {
                console.log('ERROR')
            }
        });
    }
    else{
     // console.log('lower or zero');
      $(obj).val('1');
       jQuery('#cart_content').hideLoading();
       jQuery('#cart_sidebar').hideLoading();
    }




}