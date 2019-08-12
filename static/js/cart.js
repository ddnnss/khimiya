function change_cart(obj) {
 //   console.log($(obj).val());
 //   console.log($(obj).data('item_in_cart_id'));
    jQuery('#cart_content').showLoading();
    jQuery('#cart_sidebar').showLoading();
    var item_id = $(obj).data('item_in_cart_id');
    var item_number = $(obj).val();
    if (parseInt(item_number) > 0){
        var url = '/cart/update_cart/';
        var csrf_token = $('#dummy_form [name="csrfmiddlewaretoken"]').val();
 //   console.log(csrf_token);
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
            //    console.log('OK');
                // console.log(data.all_items);
                 $('.cart_table_lg').empty();

                $.each(data.all_items,function (k,v) {
                    $('.cart_table_lg').append('<tr class="miniCartProduct">\n' +
                        '                                    <td style="width:20%" class="miniCartProductThumb">\n' +
                        '                                        <div><a href="product-details.html"> <img src="'+ v.image +'" alt="img">\n' +
                        '                                        </a></div>\n' +
                        '                                    </td>\n' +
                        '                                    <td style="width:40%">\n' +
                        '                                        <div class="miniCartDescription">\n' +
                        '                                            <h4><a href="product-details.html">'+ v.name +'</a></h4>\n' +
                        '                                            <div class="price"><span> '+ v.price +' &#8381;</span></div>\n' +
                        '                                        </div>\n' +
                        '                                    </td>\n' +
                        '                                    <td style="width:10%" class="miniCartQuantity"><a> X '+ v.number+' </a></td>\n' +
                        '                                    <td style="width:15%" class="miniCartSubtotal"><span> '+ v.total_price +' &#8381;</span></td>\n' +
                        '                                    <td style="width:5%" class="delete"><a data-item_id="'+ v.id +'" onclick="delete_from_cart(this);return false;"> x </a></td>\n' +
                        '                                </tr>');
                });
                $('.cart_footer_lg').html('');
                $('.cart_footer_lg').append('' +
                    ' <h3 class="text-right subtotal"> ИТОГО: '+ data.total_cart_price +' &#8381; </h3>\n' +
                    '                            <a class="btn  btn-danger" href="/cart"> <i class="fa fa-shopping-cart"> </i> ПРОСМОТР КОРЗИНЫ</a><a\n' +
                    '                                class="btn  btn-primary"> ОПЛАТА</a>');
                 $('#cart_content_table').empty();
                 $('#cart_content_table').append('   <tr class="CartProduct cartTableHeader">\n' +
                     '                                <td style="width:15%"> </td>\n' +
                     '                                <td style="width:40%">Товар</td>\n' +
                     '                                <td style="width:10%" class="delete">&nbsp;</td>\n' +
                     '                                <td style="width:10%">Кол-во</td>\n' +
                     '                                <td style="width:10%">Скидка</td>\n' +
                     '                                <td style="width:15%">Всего</td>\n' +
                     '                            </tr>');

                     $.each(data.all_items,function (k,v) {
                    $('#cart_content_table').append('        <tr class="CartProduct">\n' +
                        '                                <td class="CartProductThumb">\n' +
                        '                                    <div><a href="#"><img src="'+ v.image +'" alt="img"></a>\n' +
                        '                                    </div>\n' +
                        '                                </td>\n' +
                        '                                <td>\n' +
                        '                                    <div class="CartDescription">\n' +
                        '                                        <h4><a href="#">'+ v.name +'</a></h4>\n' +
                        '                                        <span class="size">'+ v.subcategory +'</span>\n' +
                        '\n' +
                        '                                        <div class="price"><span>'+ v.price +' &#8381;</span></div>\n' +
                        '                                    </div>\n' +
                        '                                </td>\n' +
                        '                                <td class="delete"><a onclick="delete_from_main_cart('+ v.id +');return false;" title="Удалить"> <i\n' +
                        '                                        class="glyphicon glyphicon-trash fa-2x"></i></a></td>\n' +
                        '                                <td><input class="form-control" data-item_in_cart_id="'+ v.id +'" onchange="change_cart(this);return false;" type="number" min="1" value="'+ v.number +'" "></td>\n' +
                        '                                <td>'+ v.discount +'</td>\n' +
                        '                                <td class="price">'+ v.total_price +' &#8381;</td>\n' +
                        '                            </tr>');
                        });
                $('.cart_total_lg').html(data.total_cart_price);
                $('#cart_subtotal_price_side').html(data.total_cart_price + ' &#8381;');
                $('#cart_total_price_side').html(data.total_cart_price_with_discount + ' &#8381;');
                $('#promo_value').html(data.promo_discount_value + ' %');

                jQuery('#cart_content').hideLoading();
                jQuery('#cart_sidebar').hideLoading();
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