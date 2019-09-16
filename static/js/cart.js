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
                    $('#cart_body').empty()
                    $.each(data.all_items,function (k,v) {
                        $('#cart_body').append(`   <tr class="main-cart-item">
                    <td>
                        <div class="main-cart-item-name">
                            <img src="${v.image}" alt=""> <span>${v.name} ${v.volume} л</span>
                        </div>

                    </td>
                    <td class="main-cart-item-number">
                        <div class="custom-input main-cart">
                            <button class="custom-input-minus" data-item_id="${v.id}" onclick="mainCartMinusItem(this)">-</button>
                            <input id="${v.id}_item_total" data-item_in_cart_id="${v.id}" value="${v.number}" disabled onchange="change_cart(this)">
                            <button class="custom-input-plus" data-item_id="${v.id}" onclick="mainCartPlusItem(this)">+</button>

                        </div>
                    </td>
                    <td class="main-cart-item-price">${numberWithCommas(v.price)} &#8381;</td>
                    <td class="main-cart-item-total-price">${numberWithCommas(v.total_price)} &#8381;</td>
                    <td class="main-cart-item-action"><a class="cart-delete-btn" onclick="delete_from_main_cart(${v.id})" href="javascript:void(0)"><span>&#10006;</span></a></td>
                </tr>`)

                    });
                    $('#cart_body').append(`<tr class="main-cart-footer">
                    <td class="main-cart-footer__total">Итого</td>
                    <td></td>
                    <td></td>
                    <td colspan="2" class="main-cart-footer__total-price">${numberWithCommas(data.total_cart_price)} &#8381;</td>

                </tr>`)
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