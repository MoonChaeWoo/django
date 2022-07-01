function pullWeather(){
// 현재 날씨
$.getJSON('https://api.openweathermap.org/data/2.5/weather?lat=37.5666805&lon=126.9784147&appid=d5faee6f8c4bc11172631f1315f7e755&units=metric', function(result){
    $('.ctemp').text('현재 : '+result.main.temp + '℃');
    $('.lowtemp').text('최저 :'+result.main.temp_min + '℃');
    $('.hightemp').text('최고 : '+result.main.temp_max + '℃');
    
    var weatherIconUrl = ''
    weatherIconUrl += '<img src='
    weatherIconUrl += '"http://openweathermap.org/img/wn/'
    weatherIconUrl += result.weather[0].icon
    weatherIconUrl += '.png" alt="'
    weatherIconUrl += result.weather[0].description
    weatherIconUrl +='">'
    $('.weather-icon').html(weatherIconUrl)
});
}
pullWeather()
setInterval(() => pullWeather(), 10000);