$(document).on("ready", inicio);

function inicio()
{
	$("#btnLugar").click(function(e){
			var miCSS ={
			"background": "rgba(0,177,255,1)",
			
		};
		$("header").css(miCSS);
	});

	$("#btnTrends").click(function(e){
			var miCSSRank ={
			"background": "rgba(127,0,249,1)",
			
		};
		$("header").css(miCSSRank);
		setNoActivo();
		$("#btnTrends").attr('class', 'icon-stats activo');
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
			"background": "rgba(15,101,239,1)",
			
		};
		$("header").css(miCSSRank);
		setNoActivo();
		$("#btnHome").attr('class', 'icon-home activo');
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
			"background": "rgba(247,104,6,1)",
			
		};
		$("header").css(miCSSActividad);
		setNoActivo();
		$("#btnActividad").attr('class', 'icon-users activo');
		$.ajax({
                url: '/dataactivity/',
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

	$("#btnDj").click(function(e){
			var miCSSDj={
			"background": "rgba(217,35,249,1)",
			
		};
		$("header").css(miCSSDj);
		setNoActivo();
		$("#btnDj").attr('class', 'icon-headphones activo');
		$.ajax({
                url: '/dataheydj/',
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

	$("#btnPerfil").click(function(e){
			var miCSSPerfil={
			"background": "#D8B900",
			
		};
		$("header").css(miCSSPerfil);
		setNoActivo();
		$("#btnPerfil").attr('class', 'icon-user activo');
	});

	$("#btnPost").click(function(e){
		setNoActivo();
		$.ajax({
            url: '/postphoto/',
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
	
}

var setNoActivo = function eliminarActivo(){
	$("#menu li").each(function(){
		$("#menu>li>a").removeClass("activo");
	});
}




