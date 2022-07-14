$(document).ready(function () {
    $(".loginfalse").hide()
    $(".loginture").hide()
    check_login()
    // set_temp()
})

// 로그인 여부 확인 함수
function check_login() {
    console.log("login check")
    $.ajax({
        type: 'POST',
        url: '/islogin',
        data: {},
        success: function (response) {
            let result = response['result'];
            let success = result['success'];
            if (success == 'true') {
                $('.loginture').show();
            } else {
                $('.loginfalse').show();
            }
        }
    });
}

// 로그아웃 함수
function logout() {
    console.log($.removeCookie('mytoken', {path: '/'}))
    $.removeCookie('mytoken', {path: '/'});
    window.location.href = '/login'
}