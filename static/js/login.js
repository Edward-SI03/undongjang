$(document).ready(function () {
    set_temp()
});

let id = $("#idenfier")
let pw = $("#password")

// 로그인 시도 버튼
function login() {
    $.ajax({
        type: "POST",
        url: "/login",
        data: {
            id_give: id.val(),
            pw_give: pw.val()
        },
        success: function (response) {
            if (response["result"] == "success") {
                // 서버에서 로그인 정보가 일치하면 토큰 정보를 받아 쿠키로 로그인토큰을 생성(head에 cookie 생성하는 CDN 필요)
                // 콘솔창 옆 애플리케이션 탭 쿠키 탭에서 생성된 로그인 정보 쿠키 확인 가능
                $.cookie('mytoken', response['token']), {path: '/'};
                alert(response['msg'])
                window.location.replace("/")
            } else {
                alert(response['msg'])
                return
            }

        }
    })
}

// 잠깐 회원가입처럼 디비 저장해서 로그인기능 확인하기위해 만든것 나중에 회원가입페이지로 이동 버튼으로 사용예정
// function create() {
//     $.ajax({
//         type: "POST",
//         url: "/create",
//         data: {
//             id_give: id.val(),
//             pw_give: pw.val()
//         },
//         success: function (response) {
//             console.log(response)
//         }
//     })
// }