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
                    if ($('footer').length){
                    	//alert('Si hay!');
                    } else {
                    	//alert('No hay!');
                    	recrearFooter();
                    }
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
                    if ($('footer').length){
                    	//alert('Si hay!');
                    } else {
                    	//alert('No hay!');
                    	recrearFooter();
                    }

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
                    if ($('footer').length){
                    	//alert('Si hay!');
                    } else {
                    	//alert('No hay!');
                    	recrearFooter();
                    }
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
                    $('#formulario').remove();
                    if ($('footer').length){
                    	//alert('Si hay!');
                    } else {
                    	//alert('No hay!');
                    	recrearFooter();
                    }
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
                //$('header').remove();
                $('footer').remove();
                $('#contenido').append(result);
            },
              //   error: function (xhr, ajaxOptions, thrownError) {
              //   alert(xhr.status);
              //   alert(thrownError);
              // }
        });
	});

    $("#btnSetting").click(function(e){
        setNoActivo();
        $.ajax({
            url: '/settings/',
            type: 'GET',
            data: {
                
            },
            traditional: true,
            dataType: 'html',
            success: function(result) {
                timer.stop();
                $('#cosasLocas').remove();
                $('#asyncContainer').remove();
                //$('header').remove();
                $('footer').remove();
                $('#contenido').append(result);
            },
              
        });
    });

    var formLogin = $("#formLodasdasdsgin");
    $(formLogin).on('submit',function(){
        $.ajax({
                data: $(formLogin).serialize(),
                type: $(formLogin).attr('method'),
                dataType: "json",
                url: $(formLogin).attr('action'),
                success: function(data) {
                    if (data.codigo == 2) {
                        //mostrarMensaje(formLogin, "<span class='alertContenido'><strong>Alto!</strong> El usuario o contraseña ingresado no es valido.</span>", "alert-danger");
                        alert("You have entered an incorrect email or password.");
                    } else if (data.codigo == 1) {
                        window.location = '/home/';
                    }
                }
            });
            return false;
    });
	
}

var setNoActivo = function eliminarActivo(){
	$("#menu li").each(function(){
		$("#menu>li>a").removeClass("activo");
	});
}

var recrearFooter = function noFooter(){
	var footerHtml = '<footer>';
        footerHtml += '<ul>';
        footerHtml += '<li><a id="btnPost" class="icon-quill icono" href="#"><br><div class="letraicono">Post</div></a></li>';
        footerHtml += '<li><a class="icon-music icono" href=""><br><div class="letraicono">Music</div></a></li>';
        footerHtml += '<li><a class="icon-spinner icono" href=""><br><div class="letraicono">Refresh</div></a></li>';
        footerHtml += '<li><a class="icon-cog icono" href=""><br><div class="letraicono">Settings</div></a></li>';
        footerHtml += '</ul>';
        footerHtml += '</footer>';
        footerHtml += "<script type='text/javascript'>$('#btnPost').click(function(e){setNoActivo();$.ajax({url: '/postphoto/',type: 'GET',data: {},traditional: true,dataType: 'html',success: function(result) {timer.stop();$('#cosasLocas').remove();$('#asyncContainer').remove();$('footer').remove();$('#contenido').append(result);},});});</script>";
    $("body").append(footerHtml);
}



