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
            $('.cart_table').empty();

            $('.cart-items').text(data.total_items_in_cart)

            if (data.all_items.length > 0) {
                $.each(data.all_items,function (k,v) {
                    $('.cart_table').append(`  <tr>
                            <td >
                                <img  src="${v.image}" alt="">
                            </td>
                            <td>
                                ${v.name} ${v.volume} л
                            </td>
                            <td>
                                <span id="cart_item_number">${v.number} шт</span> x  <span id="cart_item_price">${numberWithCommas(v.price)} &#8381;</span> = <span id="cart_item_total_price">${numberWithCommas(v.total_price)} &#8381;</span>
                            </td>
                        <td>
                            <a class="cart-delete-btn" href="javascript:void(0)"
                               data-item_id="${v.id}"
                               onclick="delete_from_cart(this)"><span>&#10006;</span></a>
                        </td>
                        </tr>`)


                });
                $('.cart_table').append(` <tr class="cart-footer">
                            <td colspan="4">Итого: ${numberWithCommas(data.total_cart_price)} &#8381;</td>
                        </tr>
                        <tr>
                            <td colspan="4">
                                <a href="/cart/" class="btn btn-sm">Открыть корзину</a>
                                <a href="/checkout/" class="btn-outline btn-sm">Оплата</a>
                            </td>
                        </tr>`)

            }
            else
            {
                $('.cart-items').css('display','none')
                $('.cart_table').append(` <tr>
                          <td style="width: 100% !important;"> Корзина пуста</td>
                          </tr>`);

            }
        },
        error: function () {
            console.log('ERROR')
        }
    });
    console.log($(del).data('item_id'));
    // $(del).closest('li').remove();
}
