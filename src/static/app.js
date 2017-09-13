function updateMap(zipcode){
    src="//www.google.com/maps/embed/v1/place?"+
    "zoom=12&key=AIzaSyA6QG8IoU0eQulNezQScWTgtH7zdf-6MU0&q="+zipcode
    map=$("iframe#map")
    map.attr("src",src)
    $("table#zchart tr.highlight").each(function () {
        $(this).removeClass('highlight');
    })
    $("tr"+"#z"+zipcode).addClass('highlight');
}
