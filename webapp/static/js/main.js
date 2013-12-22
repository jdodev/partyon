$(document).on("ready", inicio);

function inicio()
{
	$("#btnLugar").click(function(e){
			var miCSS ={
			"background": "rgba(0,177,255,0.9)",
			
		};
		$("header").css(miCSS);
	});

	$("#btnTrends").click(function(e){
			var miCSSRank ={
			"background": "rgba(127,0,249,0.9)",
			
		};
		$("header").css(miCSSRank);
		setNoActivo();
		$("#btnTrends").attr('class', 'activo');
		$.ajax({
                url: '/datatrends/',
                type: 'GET',
                data: {
                    
                },
                traditional: true,
                dataType: 'html',
                success: function(result) {
                    timer.stop();
                    $('#cosasLocas').remove();
                    $('#asyncContainer').remove();
                    $('#contenido').append(result);
                },
                  //   error: function (xhr, ajaxOptions, thrownError) {
                  //   alert(xhr.status);
                  //   alert(thrownError);
                  // }
            });
	});

	$("#btnHome").click(function(e){
			var miCSSRank ={
			"background": "rgba(15,101,239,0.9)",
			
		};
		$("header").css(miCSSRank);
		setNoActivo();
		$("#btnHome").attr('class', 'activo');
		$.ajax({
                url: '/datahome/',
                type: 'GET',
                data: {
                    
                },
                traditional: true,
                dataType: 'html',
                success: function(result) {
                    timer.stop();
                    $('#cosasLocas').remove();
                    $('#asyncContainer').remove();
                    $('#contenido').append(result);
                },
                  //   error: function (xhr, ajaxOptions, thrownError) {
                  //   alert(xhr.status);
                  //   alert(thrownError);
                  // }
            });
	});

	$("#btnActividad").click(function(e){
			var miCSSActividad={
			"background": "rgba(247,104,6,0.9)",
			
		};
		$("header").css(miCSSActividad);
		setNoActivo();
		$("#btnActividad").attr('class', 'activo');
	});

	$("#btnDj").click(function(e){
			var miCSSDj={
			"background": "rgba(217,35,249,0.9)",
			
		};
		$("header").css(miCSSDj);
		setNoActivo();
		$("#btnDj").attr('class', 'activo');
	});

	$("#btnPerfil").click(function(e){
			var miCSSPerfil={
			"background": "rgba(247,213,13,0.9)",
			
		};
		$("header").css(miCSSPerfil);
		setNoActivo();
		$("#btnPerfil").attr('class', 'activo');
	});
	
}

var setNoActivo = function eliminarActivo(){
	$("#menu li").each(function(){
		$("#menu>li>a").removeClass("activo");
	});
}




