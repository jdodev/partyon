$(function(){
	var LAT = 13.30272;
	var LNG = -87.174107;

	if (navigator.geolocation)
	{
		navigator.geolocation.getCurrentPosition(getPosition, getError);
	} else {
		alert(":'(  Your browser does not support geolocation.");
		$("#Localizado").val(092212);
	}

	function getPosition(position)
	{
		var lat = position.coords.latitude;
		var lng = position.coords.longitude;

		$("#Localizado").val(123821);
		$("#Latitud").val(lat);
		$("#Longitud").val(lng);

		alert($("#Latitud").val() + ' ' + $("#Longitud").val());
	}

	function getError(err)
	{
		alert(":'(  We were unable to locate you, try again later. ERROR.");
		$("#Localizado").val(092212);
		$("#Latitud").val(786677);
		$("#Longitud").val(231231);
	}
});