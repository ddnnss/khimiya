function wishlist_add(item_id) {
    console.log(item_id);
      var csrf_token = $('#dummy_form [name="csrfmiddlewaretoken"]').val();
    // console.log($(form).attr('action'));
    //  console.log(csrf_token);
        var data = {};
        if (item_id){
            data.item_id = item_id;
        }
        else{
            data.item_id = $('#item_id').val();
        }

        data['csrfmiddlewaretoken'] = csrf_token;
        var url = '/cart/wishlist_add/';
        console.log(data);
        $.ajax({
            url:url,
            type:'POST',
            data: data,
            cache:true,
            success: function (data) {
                console.log('OK');
                $('#item_add_wishlist').attr('disabled','disabled');
                console.log(data.result);

                if (data.result){
                    $.amaran({
                            'theme'     :'colorful',
                            'content'   :{
                               bgcolor:'#38f28d',
                               color:'#fff',
                               message:'Товар добавлен в закладки !'
                            },
                            'position'  :'bottom right',
                            'outEffect' :'slideBottom'
                        });
                    $('#quick_view_wish_button').css('display','none')
                }
                else
                {
                     $.amaran({
                            'theme'     :'colorful',
                            'content'   :{
                               bgcolor:'#f23c3a',
                               color:'#fff',
                               message:'Недоступно для незарегистрированных пользователей !'
                            },
                            'position'  :'bottom right',
                            'outEffect' :'slideBottom'
                        });
                }


            },
            error: function () {
                console.log('ERROR')
            }
        })
}

function wishlist_delete(id) {
    console.log(id);
     var csrf_token = $('#dummy_form [name="csrfmiddlewaretoken"]').val();
    // console.log($(form).attr('action'));
    //  console.log(csrf_token);
        var data = {};
        data.id = id;
        data['csrfmiddlewaretoken'] = csrf_token;
        var url = '/cart/wishlist_delete/';
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
                    $('#wl_'+id).remove();
                    $.amaran({
                            'theme'     :'colorful',
                            'content'   :{
                               bgcolor:'#38f28d',
                               color:'#fff',
                               message:'Товар удален из закладок !'
                            },
                            'position'  :'bottom right',
                            'outEffect' :'slideBottom'
                        });
                }



            },
            error: function () {
                console.log('ERROR')
            }
        })

}

function qwerty() {
    if ($('.search-menu-bar').hasClass('search-menu-open')){
        $('.search-menu-bar').removeClass('search-menu-open');
    }
    else {
       $('.search-menu-bar').addClass('search-menu-open');
    }

}

 $(".search-trigger").on('click', function (e) {
        $('.search-overly-mask').toggleClass("open"); //you can list several class names
        e.preventDefault();
    });

    $(".search-overly-close-trigger").on('click', function (e) {
        $('.search-overly-mask').removeClass("open"); //you can list several class names
        e.preventDefault();
    });
