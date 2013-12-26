$(function(){
	var LAT = 13.30272;
	var LNG = -87.174107;

	if (navigator.geolocation)
	{
		navigator.geolocation.getCurrentPosition(getPosition, getError);
	} else {
		alert(":'(  Your browser does not support geolocation.");
	}

	function getPosition(position)
	{
		var lat = position.coords.latitude;
		var lng = position.coords.longitude;

		alert(lat + " " + lng)

		$("#Latitud").val(lat);
		$("#Longitud").val(lng);
	}

	function getError(err)
	{
		alert(":'(  We were unable to locate you, try again later. ERROR.");
	}
});