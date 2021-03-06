sessionStorage.clear();

$(document).ready(function(){
   $('#submitSlika').click(function(){
      $('#formaReg').submit()
   })
});

$(document).ready(function(){
   $('#submitLog').click(function(){
      $('#formaLog').submit()
   })
});

$(document).ready(function(){
   $('#pretragaBTN').click(function(){
      $('#pretraga').submit()
   })
})

/*
$(document).ready(function(){
   $('#myBtn').click(function(){
      $('#logoutForm').submit()
   })
})
*/

$("#biznisButton").click(function(){
	if($('.zadnjiPoslovi__last--navigator--left').css('margin-left') == '140px'){
		$('.zadnjiPoslovi__last--navigator--left').css('animation', 'prebaciDesno 0.5s ease-out 0s 1 normal forwards running');
		$('#b2c').addClass('hidden');
		$('#b2b').removeClass('hidden');
	}
});
$("#posaoButton").click(function(){
	if($('.zadnjiPoslovi__last--navigator--left').css('margin-left') == '435px'){
		$('.zadnjiPoslovi__last--navigator--left').css('animation', 'prebaciLijevo 0.5s ease-out 0s 1 normal forwards running');
		$('#b2b').addClass('hidden');
		$('#b2c').removeClass('hidden');
	}
});

setInterval(function(){
	setTimeout(function(){
		document.getElementById("lijevo").style.animation = "naCentar 0.7s ease-out 0s 1 normal forwards running";
		document.getElementById("centar").style.animation = "okreni 1s ease-out 0s 1 normal forwards running";
		document.getElementById("desno").style.animation = "atomskiDesno 1s ease-out 0s 1 normal forwards running";
		document.getElementById('cijenaRada').innerHTML = "1200";
		document.getElementById('traziSe').innerHTML = "Traži se <strong>vodoinstalater</strong> na području Cazina!";
		$('.zadnjiPoslovi__popularno--dots div:nth-child(2)').removeClass('active');
		$('.zadnjiPoslovi__popularno--dots div:nth-child(3)').addClass('active');
}, 1000);
 
	setTimeout(function(){
		document.getElementById("lijevo").style.animation = "okreni2 1s ease-out 0s 1 normal forwards running";
		document.getElementById("centar").style.animation = "okreni3 1s ease-out 0s 1 normal forwards running";
		document.getElementById("desno").style.animation = "okreni4 0.7s ease-out 0s 1 normal forwards running";
		document.getElementById('cijenaRada').innerHTML = "1500";
		document.getElementById('traziSe').innerHTML = "Traži se <strong>mladi policajac</strong> na području Sarajeva!";
		$('.zadnjiPoslovi__popularno--dots div:nth-child(3)').removeClass('active');
		$('.zadnjiPoslovi__popularno--dots div:nth-child(1)').addClass('active');
	}, 3000);

	setTimeout(function(){
		document.getElementById("desno").style.animation = "okreni5 1s ease-out 0s 1 normal forwards running";
		document.getElementById("lijevo").style.animation = "okreni6 1s ease-out 0s 1 normal forwards running";
		document.getElementById("centar").style.animation = "okreni7 0.7s ease-out 0s 1 normal forwards running";
		document.getElementById('cijenaRada').innerHTML = "1700";
		document.getElementById('traziSe').innerHTML = "Traži se <strong>komercijalista</strong> na području Mostara!";
		$('.zadnjiPoslovi__popularno--dots div:nth-child(1)').removeClass('active');
		$('.zadnjiPoslovi__popularno--dots div:nth-child(2)').addClass('active');
		// document.getElementById("biz").style.animation = "slikaChange 0.7s ease-out 0s 1 normal forwards running";
	}, 5000);
}, 6000);

$(document).ready(function() {
    $('.goToTop').click(function(){
        $('html, body').animate({scrollTop:0}, 'slow');
        return false;
    });
});

$('#osobaSector').click(function(){
		$('.regBox').css('height', '714px !important');
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
			document.getElementById("vrsta").value = "radnik"
		}
		if($(window).width() > 1168){
				$('.regBox').css('height', '542px');
			} else if($(window).width() < 1168){
				$('.regBox').css('height', '714px');
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
			if($(window).width() > 1168){
				$('.regBox').css('height', '670px');
			} else if($(window).width() < 1168){
				$('.regBox').css('height', '920px');
			}
			$('.regBox__lijevo--box').css('height', '361px');
			$('.regBox__lijevo').css('display', 'block !important');
			document.getElementById("vrsta").value = "firma"
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

	function stopMobileScroll() {
    document.ontouchmove = function (e) {
        e.preventDefault();
    };
};

function enableMobileScroll() {
    document.ontouchmove = function () {
        return true;
    };
};

$('.testmoniali__kucice').owlCarousel({
	autoplay: true,
	center: true,
	loop: true,
	touchDrag  : false,
    mouseDrag  : true,
    onDrag: stopMobileScroll,
    onDragged: enableMobileScroll
});

var modal = document.getElementById('myModal');
var btn = document.getElementById("myBtn");
var span = document.getElementsByClassName("close")[0];
var span2 = document.getElementsByClassName("close")[1];
var span3 = document.getElementsByClassName("close")[2];

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

var modal3 = document.getElementById('myModal3');
var btn3 = document.getElementById("myBtn3");
btn3.onclick = function() { modal3.style.display = "block"; }
span3.onclick = function() { modal3.style.display = "none"; }
window.onclick = function(event) {
    if (event.target == modal3) { modal3.style.display = "none"; }
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

