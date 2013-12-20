$(document).on("ready", inicio);

function inicio()
{
	$("#btnLugar").click(function(e){
			var miCSS ={
			"background": "rgba(0,177,255,0.9)",
			
		};
		$("header").css(miCSS);
	});

	$("#btnRank").click(function(e){
			var miCSSRank ={
			"background": "rgba(127,0,249,0.9)",
			
		};
		$("header").css(miCSSRank);
	});

	$("#btnActividad").click(function(e){
			var miCSSActividad={
			"background": "rgba(247,104,6,0.9)",
			
		};
		$("header").css(miCSSActividad);
	});

	$("#btnDj").click(function(e){
			var miCSSDj={
			"background": "rgba(217,35,249,0.9)",
			
		};
		$("header").css(miCSSDj);
	});

	$("#btnPerfil").click(function(e){
			var miCSSPerfil={
			"background": "#2E2E2E",
			
		};
		$("header").css(miCSSPerfil);
	});
	
}