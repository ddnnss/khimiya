function delete_from_cart(del){

    var item_id = $(del).data('item_id');
    var url = '/cart/delete_from_cart/';
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
            success: function (data) {
                console.log('OK');
                console.log(data.all_items);
                $('.cart_table_lg').empty();
                if (data.all_items.length > 0) {
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
                    $('.cart_total_lg').html(data.total_cart_price);
                    $('.cart_footer_lg').html('');
                    $('.cart_footer_lg').append(' <h3 class="text-right subtotal"> ИТОГО: '+ data.total_cart_price +' &#8381; </h3>\n' +
                    '                            <a class="btn  btn-danger" href="/cart"> <i class="fa fa-shopping-cart"> </i> ПРОСМОТР КОРЗИНЫ</a><a\n' +
                    '                                class="btn  btn-primary"> ОПЛАТА</a>');
                }
                else
                {
                    $('.cart_total_lg').html('0');
                    $('.cart_footer_lg').html('');
                    $('.cart_footer_lg').append('<h3 class="text-right subtotal"> КОРЗИНА ПУСТА </h3>');
                    $('#checkout_btn').attr('disabled','disabled');
                }
            },
            error: function () {
                console.log('ERROR')
            }
        });
console.log($(del).data('item_id'));
 // $(del).closest('li').remove();
}
