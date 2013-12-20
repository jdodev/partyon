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
	});

	$("#btnHome").click(function(e){
			var miCSSRank ={
			"background": "rgba(15,101,239,0.9)",
			
		};
		$("header").css(miCSSRank);
		setNoActivo();
		$("#btnHome").attr('class', 'activo');
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
			"background": "#2E2E2E",
			
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




