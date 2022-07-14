// 날씨 api 이용 실시간 온도 받아오기
function set_temp() {
    $.ajax({
        type: "GET",
        url: "http://spartacodingclub.shop/sparta_api/weather/seoul",
        data: {},
        success: function (response) {
            let temps = response['temp']
            temps = Math.ceil(temps * 10) /10
            $('.temp').text(temps)
        }
    })
}