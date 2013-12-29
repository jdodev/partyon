$(function(){
	var LAT = 13.30272;
	var LNG = -87.174107;

	$("#cargandoModal").attr('class', 'siCargaModal');

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

		DataHome();
		//alert($("#Latitud").val() + ' ' + $("#Longitud").val());
	}

	function getError(err)
	{
		$("#cargandoModal").attr('class', 'noCargaModal');
		alert(":'(  We were unable to locate you, try again later. ERROR.");
		$("#Localizado").val(092212);
		$("#Latitud").val(786677);
		$("#Longitud").val(231231);
	}

	var DataHome = function(){
	    $.ajax({
	        url: '/datahome/',
	        type: 'GET',
	        data: {
	            
	        },
	        traditional: true,
	        dataType: 'html',
	        success: function(result) {
	            //alert(result);
	            //alert("Home");
	            $('#cosasLocas').remove();
	            $('#asyncContainer').remove();
	            $('#contenido').append(result);
	            $("#cargandoModal").attr('class', 'noCargaModal');
	        },
	          //   error: function (xhr, ajaxOptions, thrownError) {
	          //   alert(xhr.status);
	          //   alert(thrownError);
	          // }
	    });
	};
});