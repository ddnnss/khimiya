function add_to_cart(el) {

    let item_number = document.getElementById('item_total').value
    let item_id = el.dataset.item_id
    let item_name = el.dataset.item_name
    let item_image = el.dataset.item_image
    let item_unit = el.dataset.item_unit
    let item_volume = parseFloat(document.getElementsByClassName('select-selected')[0].innerHTML)
    let csrf_token = $('#dummy_form [name="csrfmiddlewaretoken"]').val();
    let data = {};
    data.item_id = item_id;
    data.item_number = item_number;
    data.item_volume = item_volume
    data['csrfmiddlewaretoken'] = csrf_token;
    let url = '/cart/add_to_cart/';
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
                $('.cart_table').append(`  <tr>
                            <td >
                                <img  src="${v.image}" alt="">
                            </td>
                            <td>
                                ${v.name} ${v.volume} ${v.unit}
                            </td>
                            <td>
                                <span id="cart_item_number">${v.number} шт</span> x  <span id="cart_item_price">${v.price} &#8381;</span> = <span id="cart_item_total_price">${v.total_price} &#8381;</span>
                            </td>
                        <td>
                            <a class="cart-delete-btn" href="javascript:void(0)"
                               data-item_id="${v.id}"
                               onclick="delete_from_cart(this)"><span>&#10006;</span></a>
                        </td>
                        </tr>`)
            });
            $('.cart_table').append(` <tr class="cart-footer">
                            <td colspan="4">Итого: ${data.total_cart_price} &#8381;</td>
                        </tr>
                        <tr>
                            <td colspan="4">
                                <a href="/cart/" class="btn btn-sm">Открыть корзину</a>
                                <a href="/checkout/" class="btn-outline btn-sm">Оплата</a>
                            </td>
                        </tr>`)
            $.amaran({
                'theme'     :'user blue',
                'content'   :{
                    img: item_image,
                    user:'Добавлено в корзину:',
                    message:`${item_number} ед. ${item_name} ${item_volume} ${item_unit}`
                },

                'position'  :'bottom right',
                'outEffect' :'slideRight'
            });
        },
        error: function () {
            console.log('ERROR')
        }
    })
}