function login(){
    email = document.getElementById("login-email").value;
    password = document.getElementById("login-password").value;
    csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    $("#errorlogin").html("");
    $.ajax({
        type:"POST",
        url:'/user/log_in/',
        data:{
            'csrfmiddlewaretoken': csrfmiddlewaretoken,
            'email':email,
            'password':password,
        },
        success : function(data){
            console.log(data);
            if(data['result'] == "success"){
                location.reload();
            }
            else if(data['result'] == "inactive"){
                $("#errorlogin").html("Please verify this E-mail address.");
            }
            else{
                $("#errorlogin").html("Проверьте введеные данные!");
            }
        }
    });
}

function signup(){

    $("#erroremail").html('')
    $("#errorpass").html('')
    $("#errorother").html('');


    $('#reg_answer').removeClass('error-field')
     $('#reg_email').removeClass('error-field')
     $('#reg_pass1').removeClass('error-field')
     $('#reg_pass2').removeClass('error-field')


    if($('#reg_answer').val()===''){
        $('#reg_answer').addClass('error-field')
        return
    }
    email = document.getElementById("reg_email").value;
    //    user_name = document.getElementById("reg_name").value;
    //   phone = document.getElementById("reg_phone").value;
    password1 = document.getElementById("reg_pass1").value;
    password2 = document.getElementById("reg_pass2").value;
    n1 = $('#reg_n1').data('n1');
    n2 = $('#reg_n2').data('n2');
    answer = $('#reg_answer').val();
    csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    $("#erroremail").html("");
    $("#errorpass").html("");

    $.ajax({
        type:"POST",
        url:'/user/signup/',
        data:{
            'csrfmiddlewaretoken': csrfmiddlewaretoken,
            'email':email,
            //     'name':user_name,
            //     'phone':phone,
            'password1':password1,
            'password2':password2,
            'n1':n1,
            'n2':n2,
            'answer':answer,
        },
        success : function(data){
            console.log(data['result']);
            if (data['result'] == "bad"){
                $("#errorother").html("Неверный ответ");
                  $('#reg_answer').addClass('error-field')
                return;
            }

            if(data['result'] == "success"){
                // $('#reg_text1').css('display','none');
                // $('#reg_text2').css('display','block');
                //location.reload();
                window.location.href = ('/user/account/edit');

            }
            else{
                if("email" in data['result']){
                     $("#erroremail").html(data['result']['email'][0]);
                    $('#reg_email').addClass('error-field')
                }

                if("password2" in data['result']){
                    $("#errorpass").html(data['result']['password2'][0]);

                     $('#reg_pass1').addClass('error-field')
                     $('#reg_pass2').addClass('error-field')
                }

            }
        }
    })

}



function restore(){
    email = document.getElementById("restore-email").value;

    csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    $("#errorrestore").html("");
    $("#okrestore").html("");
    $('#restore_btn').attr('disabled','disabled');
    $.ajax({
        type:"POST",
        url:'/user/restore/',
        data:{
            'csrfmiddlewaretoken': csrfmiddlewaretoken,
            'email':email,

        },
        success : function(data){
            console.log(data);
            if(data['result']){
                $("#okrestore").html("Новый пароль отправлен на Вашу почту!");
                $('#restore_btn').attr('disabled','disabled');
            }
            else{
                $("#errorrestore").html("Пользователь не найден!");
                $('#restore_btn').removeAttr('disabled');
            }
        }
    });
}