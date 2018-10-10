$("#biznisButton").click(function(){
	if($('.zadnjiPoslovi__last--navigator--left').css('margin-left') == '140px'){
		$('.zadnjiPoslovi__last--navigator--left').css('animation', 'prebaciDesno 0.5s ease-out 0s 1 normal forwards running');
		console.log($('#b2c'));
		$('#b2c').addClass('hidden');
		$('#b2b').removeClass('hidden');
	}
});
$("#posaoButton").click(function(){
	if($('.zadnjiPoslovi__last--navigator--left').css('margin-left') == '340px'){
		$('.zadnjiPoslovi__last--navigator--left').css('animation', 'prebaciLijevo 0.5s ease-out 0s 1 normal forwards running');
		$('#b2b').addClass('hidden');
		$('#b2c').removeClass('hidden');
	}
});


$(document).ready(function() {
    $('.goToTop').click(function(){
        $('html, body').animate({scrollTop:0}, 'slow');
        return false;
    });
});

$('#srednjiElement').toggle();
	$('#osobaSector').click(function(){
		if(!$('#osobaSector').hasClass("active")){
			$('#osobaSector').addClass("active");
			$('#firmaSector').removeClass("active");
			$('.linijaActive').css('animation', 'aktivirajGore 0.5s ease-out 0s 1 normal forwards running');
			$('#naslovTekst').text('REGISTRACIJA OSOBE');
			$('#prviInput').text('Vaše ime');
			$('#drugiInput').text('Prezime');
			$('#srednjiElement').addClass('hidden');
			$('#srednjiElement').toggle();
			$('.regBox').css('height', '542px');
		}
	});
	$('#firmaSector').click(function(){
		if(!$('#firmaSector').hasClass("active")){
			$('#firmaSector').addClass("active");
			$('#osobaSector').removeClass("active");
			$('.linijaActive').css('animation', 'aktivirajDolje 0.5s ease-out 0s 1 normal forwards running');
			$('#naslovTekst').text('REGISTRACIJA FIRME');
			$('#prviInput').text('Naziv firme');
			$('#drugiInput').text('ID broj');
			$('#srednjiElement').removeClass('hidden');
			$('#srednjiElement').toggle();
			$('.regBox').css('height', '670px');
			$('.regBox__lijevo--box').css('height', '361px');
			$('.regBox__lijevo').css('display', 'block !important');
		}
	});

	$('input').focus(function(){
		$(this).parents('.form-group').addClass('focused');
		$(this).parents('.form-group').removeClass('neaktivan');  
	});

	$('input').blur(function(){

  	var inputValue = $(this).val();

	if ( inputValue == "" ) {
		$(this).removeClass('filled');
		$(this).parents('.form-group').removeClass('focused');  
	} else {
		$(this).addClass('filled');
		$(this).parents('.form-group').addClass('neaktivan');  
	}
});

$('.testmoniali__kucice').owlCarousel({
	autoplay: true,
	center: true,
	loop: true,
});

var modal = document.getElementById('myModal');
var btn = document.getElementById("myBtn");
var span = document.getElementsByClassName("close")[0];
var span2 = document.getElementsByClassName("close")[1];
btn.onclick = function() { modal.style.display = "block";  }
span.onclick = function() {
    modal.style.display = "none";
    modal2.style.display = "none";
}
window.onclick = function(event) {
    if (event.target == modal) { modal.style.display = "none"; }
}

var modal2 = document.getElementById('myModal2');
var btn2 = document.getElementById("myBtn2");
btn2.onclick = function() { modal2.style.display = "block"; }
span2.onclick = function() { modal2.style.display = "none"; }
window.onclick = function(event) {
    if (event.target == modal2) { modal2.style.display = "none"; }
}

$('.single-kucica').mouseover(function(){
		$(this).find('.struka').css('color', '#fecd35');
		$(this).find('.struka').css('text-shadow', 'none');
		$(this).css('background-image', 'url(images/neaktivna.png)');
});
$('.single-kucica').mouseout(function(){
		$(this).find('.struka').css('color', '#eeede7');
		$(this).find('.struka').css('text-shadow', '0px 5px 10px rgba(22, 22, 22, 0.25)');
		$(this).css('background-image', 'url(images/aktivna.png)');
});