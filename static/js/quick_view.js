function quick_view(item_id)
{

   var url = '/item/quick_add_to_cart/';
   var csrf_token = $('#dummy_form [name="csrfmiddlewaretoken"]').val();
   var data = {};
   data.item_id = item_id;
   data['csrfmiddlewaretoken'] = csrf_token;
   $.ajax({
            url:url,
            type:'POST',
            data: data,
            cache:true,
            success: function (data) {
                console.log('OK');
                console.log(data);
                $('#item_id').val(data.item_id);
                $('#item_image').val(data.item_images[0]);
                $('#item_name').val(data.item_name);
                $('#item_price').val(data.item_price);

                $('.product-title').html(data.item_name);
                $('.product-code').html('АРТИКУЛ : ' + data.item_article);

                if (data.item_discount > 0){
                     $('.price-standard').html(data.item_price + ' &#8381;');
                     $('.price-sales').html(data.item_price_discount + ' &#8381;');
                }
                else {
                     $('.price-standard').html('');
                     $('.price-sales').html(data.item_price + ' &#8381;');
                }
                $('.details-description p').html(data.item_description);
                $('.product-largeimg-link img').attr('src',data.item_images[0]);
                $('.modal-product-thumb').html('');

                 $.each(data.item_images,function (i,v) {
                     $('.modal-product-thumb').append(' <a id=thumb_'+ i +'   class="thumbLink">\n' +
                         '            <img onClick="a_onClick(this)" data-large='+data.item_images[i]+' alt="img" class="img-responsive" src='+ data.item_images[i] +'>\n' +
                         '        </a>');


                 })
                $('#thumb_0').addClass('selected');
                 if(data.item_present){
                     $('#add_to_cart').css('display','block');
                     $('#item_not_present').css('display','none');
                 }
                 else
                 {
                    $('#add_to_cart').css('display','none');
                     $('#item_not_present').css('display','block');
                 }

                $('#productSetailsModalAjax').modal('show');





            },
            error: function () {
                console.log('ERROR')
            }
        });


}

function a_onClick (obj) {

                console.log($(obj).attr('data-large'));
                $(".modal-product-thumb a.selected").removeClass("selected");
               $(obj).closest('a').addClass('selected');
                var largeImage = $(obj).attr('data-large');
                $(".product-largeimg").attr('src', largeImage);

            }

