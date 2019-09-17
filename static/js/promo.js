   function use_promo() {
    var promo_code = $('#promo_code').val();
     jQuery('#promo_div').showLoading();

    if (promo_code){

       var url = '/cart/use_promo/';
       var csrf_token = $('#dummy_form [name="csrfmiddlewaretoken"]').val();

      var data = {};
        data.promo_code = promo_code;
        data['csrfmiddlewaretoken'] = csrf_token;
        console.log(data);
        $.ajax({
            url:url,
            type:'POST',
            data: data,
            cache:true,
            success: function (data) {
                console.log('OK');
                console.log(data.result);

                if (data.result){

                 $('#cart_total_price_side').html(data.total_cart_price_with_discount + ' &#8381;');
                  $('#promo_value').html(data.promo_discount_value + ' %');

                   $.amaran({
                            'theme'     :'colorful',
                            'content'   :{
                               bgcolor:'#21f26a',
                               color:'#fff',
                               message:'ПРОМО-КОД УСПЕШНО ПРИМЕНЕН !'
                            },
                            'position'  :'bottom right',
                            'outEffect' :'slideBottom'
                        });
                             jQuery('#cart_sidebar').hideLoading();

                }
                else
                {
                          $.amaran({
                            'theme'     :'colorful',
                            'content'   :{
                               bgcolor:'#F26663',
                               color:'#fff',
                               message:'ПРОМО-КОД НЕ НАЙДЕН, ЗАКОНЧЕН СРОК ДЕЙСТВИЯ ИЛИ УЖЕ ПРИМЕНЕН !'
                            },
                            'position'  :'bottom right',
                            'outEffect' :'slideBottom'
                        });
                             jQuery('#cart_sidebar').hideLoading();
                }

                //  $('.cart_total_lg').html(data.total_cart_price);
                // $('#cart_subtotal_price_side').html(data.total_cart_price + ' &#8381;');
                //  $('#cart_total_price_side').html(data.total_cart_price_with_discount + ' &#8381;');
                //   $('#promo_value').html(data.promo_discount_value + ' %');
                jQuery('#cart_sidebar').hideLoading();
            },
            error: function () {
                console.log('ERROR')
            }
        });
    }
    else{
        $.amaran({
        'theme'     :'colorful',
        'content'   :{
           bgcolor:'#F26663',
           color:'#fff',
           message:'ВВЕДИТЕ ПРОМО-КОД !'
        },
        'position'  :'bottom right',
        'outEffect' :'slideBottom'
    });
         jQuery('#promo_div').hideLoading();
    }

}