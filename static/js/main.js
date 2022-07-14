/* 화면이 로딩이되면 실행하는 코드*/

$(document).ready(function () {
    set_temp()
    $(".cards").empty()
    show_cardList()
});


/* card GET 코드 */
function show_cardList() {
    $.ajax({
        type: "GET",
        url: "/getpost",
        data: {},
        success: function (response) {
            console.log(response['msg'])

            let rows = response['all_post']
            for (let i = 0; i < rows.length; i++) {
                let post_id = rows[i]["_id"]
                // let address = rows[i]['address']
                // let comment = rows[i]['comment']
                let file = "../static/postimg/" + rows[i]['file']
                let placeName = rows[i]['placeName']
                let location = rows[i]['location']
                let workout = rows[i]['workout']

                if (file == "../static/postimg/") {
                    if (workout == "헬스") {
                        file = "../static/img/헬스장.jpg"
                    } else if (workout == "수영") {
                        file = "../static/img/수영.jpg"
                    } else if (workout == "등산") {
                        file = "../static/img/등산.jpg"
                    } else if (workout == "클라이밍") {
                        file = "../static/img/클라이밍.jpg"
                    } else if (workout == "싸이클") {
                        file = "../static/img/싸이클.jpg"
                    } else if (workout == "기타") {
                        file = "../static/img/걷기.jpg"
                    } else if (workout == "크로스핏") {
                        file = "../static/img/크로스핏.jpg"
                    }
                }

                let temp_html = `<div class="card" id="${post_id}" onclick="openmodal('${post_id}')">
                                    <img src="${file}" class="card-img-top" onerror="this.src='../static/img/exercise.png'">
                                    <div class="card-body">
                                        <h3>${placeName}</h3>
                                        <h5 class="card-title" id="card_img">${workout}</h5>
                                        <p class="card-text">${location}</p>
                                    </div>  
                                </div>`
                $('.cards').append(temp_html)
            }


        }
    });
}

// 상세 모달창에 클릭시 세부 내용 보여주기
function detailmodal(post_id) {

    $.ajax({
        type: "POST",
        url: "/modal",
        data: {post_id_give: post_id,},
        success: function (response) {
            // console.log(response['result']['message'])
            let rows = response['result']['data']

            let address = rows['address']
            let comment = rows['comment']
            let file = "../static/postimg/" + rows['file']
            let location = rows['location']
            let workout = rows['workout']
            let placeName = rows['placeName']
            let userid = rows['userid']
            let post_id = rows["postid"]
            // console.log(post_id)

            if (file == "../static/postimg/") {
                if (workout == "헬스") {
                    file = "../static/img/헬스장.jpg"
                } else if (workout == "수영") {
                    file = "../static/img/수영.jpg"
                } else if (workout == "등산") {
                    file = "../static/img/등산.jpg"
                } else if (workout == "클라이밍") {
                    file = "../static/img/클라이밍.jpg"
                } else if (workout == "싸이클") {
                    file = "../static/img/싸이클.jpg"
                } else if (workout == "기타") {
                    file = "../static/img/걷기.jpg"
                } else if (workout == "크로스핏") {
                    file = "../static/img/크로스핏.jpg"
                }
            }

            let temp_html = `<div id="modalCard">
                                <div id="modalbox1">
                                    <div id="modalimgbox">
                                        <img id="modalimg" src="${file}" onerror="this.src='../static/img/exercise.png'">
                                    </div>

                                    <div id="modalinpomation">
                                        <h5>${placeName}</h5>
                                        <p>${workout}</p>
                                        <p>${location}</p>
                                        <p class="modallink">
                                            <a href="${address}"
                                               target="_blank">자세한 링크</a>
                                        </p>
                                        <p>작성자 : ${userid}</p>

                                    </div>

                                </div>
                                <div id="modalbox2">
                                    <p id="review">리뷰 : ${comment}</p>
                                </div>
                            </div>
                            <div class="modalBtn">
                                <button type="button" id="modalclose" class="modalBtn2">닫기</button>
                                <button type="button" id="modaldel" class="modalBtn2" onclick="delpostcheck('${post_id}')">삭제</button>
                            </div>`


            $('#modal').append(temp_html)
            // 링크가 없다면 아에 안보여줌
            if (address == "") {
                $(".modallink").empty()
            }
            // 아이디와 글작성자가 같지 않으면 클래스를 투가해서 삭제버튼 안보이게
            if (userID !== userid) {
                $('#modaldel').addClass("hide")
            }
        }
    })
}

/* 모달창  */

function openmodal(a) {
    detailmodal(a)
    $('#modal').css('display', 'block');
}

$('#modalBg').on('click', function () {
    $('#modal').css('display', 'none');
    // $('#modalCard').empty()
    $('#modalCard').remove()
    $(".modalBtn").remove()
})
$('#modalclose').on('click', function () {
    $('#modal').css('display', 'none');
    $('#modalCard').remove()
    $(".modalBtn").remove()
})


// 게시물 삭제 확인 알림
function delpostcheck(post_id){
    let check_del = confirm("게시물을 삭제 하시겠습니까?");

    if(check_del == true){
        delpost(post_id)
    }else{
        return
    }
}


// 게시물 삭제
function delpost(post_id) {
    // console.log(post_id)
    $.ajax({
        type: "POST",
        url: "/delpost",
        data: {post_id_give: post_id,},
        success: function (response) {
            alert(response['result']['msg'])
            window.location.replace("/")
        }
    });
}
