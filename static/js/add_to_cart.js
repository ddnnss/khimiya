function add_to_cart(form,i_id) {
    if (i_id){
       // console.log(form.elements[i_id+"_items_number"].value);
    var btn = "#"+i_id+"_submit"
    // console.log($(btn).data('item_name'));


    //     console.log(form.elements["items_number"].value);
    //     console.log(form.elements["item_id"].value);
    //     console.log(form.elements["item_name"].value);
    //     console.log(form.elements["item_price"].value);
    //     console.log(form.elements["item_image"].value);
        var item_number = form.elements[i_id+"_items_number"].value
        var item_id = $(btn).data('item_id')
        var item_name = $(btn).data('item_name')
        var item_price = $(btn).data('item_price')
        var item_image = $(btn).data('item_image')


    }
    else {
        var item_number = form.elements["items_number"].value
        var item_id = form.elements["item_id"].value
        var item_name = form.elements["item_name"].value
        var item_price = form.elements["item_price"].value
        var item_image = form.elements["item_image"].value
    }


    var csrf_token = form.elements["csrfmiddlewaretoken"].value
    // console.log($(form).attr('action'));
    //  console.log(csrf_token);
        var data = {};
        data.item_id = item_id;
        data.item_number = item_number;
        data['csrfmiddlewaretoken'] = csrf_token;
        var url = $(form).attr('action');
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
                $('.cart_total_lg').html(data.total_cart_price);
                $('.cart_footer_lg').html('');
                $('.cart_footer_lg').append('' +
                    ' <h3 class="text-right subtotal"> ИТОГО: '+ data.total_cart_price +' &#8381; </h3>\n' +
                    '                            <a class="btn  btn-danger" href="/cart"> <i class="fa fa-shopping-cart"> </i> ПРОСМОТР КОРЗИНЫ</a><a\n' +
                    '                                class="btn  btn-primary"> ОПЛАТА</a>');


                $.amaran({
                        'theme'     :'user blue',
                        'content'   :{
                            img: item_image,
                            user:'Добавлено в корзину:',
                            message: item_number + ' шт. - ' + item_name
                        },
                        'position'  :'bottom right',
                        'outEffect' :'slideBottom'
                    });
            },
            error: function () {
                console.log('ERROR')
            }
        })
    }