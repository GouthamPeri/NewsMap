marker = undefined
marker2 = undefined
markers = []
onScreenMarkers = []
map = undefined
isIdle = true;
panned = true;
page = 0


$(document).ready(function(){
    $('.parallax').parallax();
    newsItemTemplate = undefined
    $('.loader').fadeIn(400, function(){
        $.getScript('https://maps.googleapis.com/maps/api/js?key=AIzaSyCis1M1LYaOmuDEn3Ec5LKxd9tAHpgH41Q')
            .done(function(script, textStatus){
                $.get('newsitems.html', function(template){
                    newsItemTemplate = template
                    $('#news_list').hide();
                    $('.loader').hide();
                    $('#news_list').empty()
                    initMap();
                    
                });
            })
    })
    $('#news_list').on('scroll', function() {
        if($(this).scrollTop() + $(this).innerHeight()
            >= $(this)[0].scrollHeight) {
            var postData = {cities: new Array()}
            var markers = captureMarkersOnScreen()
            for(var i = 0; i < markers.length; i++) {
                postData['cities'].push(markers[i].title)
            }
            // $('#news_list').animate({
            //     scrollTop: $("#news_list").position().top
            // }, 1000);
            // START LOADING THE NEXT ITEMS
            page += 10
            $.post('api/news/' + page + '/', postData, updateNewsListDOM, 'json');    
        }
    });
});

function w3_open() {
    document.getElementById("mySidebar").style.display = "block";
}
function w3_close() {
    document.getElementById("mySidebar").style.display = "none";
}

function initMap() {
    var bounds = new google.maps.LatLngBounds(); //for display bounds

    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 5,
        center: new google.maps.LatLng(28.7041, 77.1025),
    });
    $.get('api/coords/', function(coords){
        coords = JSON.parse(coords);
        for(city in coords){
            var marker = new google.maps.Marker({
                position: coords[city],
                map: map,
                title: city
            });
            markers.push(marker);
        }

        google.maps.event.addListener(map, 'zoom_changed', function(){
            panned = true;
            updateNewsItems();
        });
        google.maps.event.addListener(map, 'dragend', function(){
            panned = true;
            updateNewsItems();
        });
        google.maps.event.addListener(map, 'idle', function(){
            isIdle = true;
            updateNewsItems();
        });
        onScreenMarkers = captureMarkersOnScreen()
        updateNewsItems()
    });
}

function isIn(s)          { return x => s.has(x); }

function contains(s1, s2) { return [...s2] . every(isIn(s1)); }

function eqSet(a, b)      { return a.size === b.size && contains(a, b); }

function updateNewsItems(){
    if(panned && isIdle){
        page = 0;
        var postData = {cities: new Array()}
        
        var tempMarkers = new Set([...(captureMarkersOnScreen())])
        var prevMarkers = new Set([...onScreenMarkers])
        console.log(tempMarkers.size)
        if(!tempMarkers.size){
            onScreenMarkers = []
            $('#news_list').fadeOut(200).html("<h4 class='text-center'><b>No News from this region!</b></h4>").fadeIn(300);
            isIdle = false;
            panned = false;
        }
        else if(eqSet(tempMarkers, prevMarkers) == false){
            $('#news_list').fadeOut(300).empty()
            onScreenMarkers = tempMarkers
            for(let marker of tempMarkers) {
                postData['cities'].push(marker.title)
            }
            $.post('api/news/' + page + '/', postData, updateNewsListDOM, 'json');    
            isIdle = false;
            panned = false;
        }
    }
}

function updateNewsListDOM(data) {
    data = JSON.parse(data)['items']
    var newsItemDom = $.tmpl(newsItemTemplate, data)
    $(newsItemDom).appendTo('#news_list');
    $('#news_list').fadeIn(500)
}

function captureMarkersOnScreen(){
    var onScreenMarkers = []
    for(var i = markers.length, bounds = map.getBounds(); i--;) {
        if( bounds.contains(markers[i].getPosition()) ){
            onScreenMarkers.push(markers[i])
        }
    }
    return onScreenMarkers
}


