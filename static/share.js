$(document).ready(()=>{
    $(".shareBtn").click((e)=>{
        e.preventDefault();
        let dataPage = e.target.getAttribute('data-page');
        let dataHref = e.target.getAttribute('data-href');
        if(!dataHref)
            dataHref = window.location.href;
        //facebook
        if(dataPage == 'fb'){
            let shareurl = "https://www.facebook.com/sharer/sharer.php?app_id=392299231338007&sdk=joey&u="+ encodeURIComponent(dataHref) +"&display=popup&ref=plugin&src=share_button";
            return !window.open(shareurl, 'Facebook', 'width=640,height=580');
        }
        //instagram - ne dozvoljava ig
        // else if(dataPage == 'ig'){}
        //whatsapp
        else if(dataPage == 'wa'){
            location.href = 'whatsapp://send?text='+dataHref;
        }
        //linkedin
        else if(dataPage == 'ln'){
            let shareurl = "https://www.linkedin.com/shareArticle?mini=true&url="+encodeURIComponent(dataHref)+"&summary=&source=ZIZA.ba";
            !window.open(shareurl, 'Facebook', 'width=640,height=580');
        }
        //viber
        else if(dataPage == 'vb'){
            location.href = "https://3p3x.adj.st/?adjust_t=u783g1_kw9yml&adjust_fallback=https%3A%2F%2Fwww.viber.com%2F%3Futm_source%3DPartner%26utm_medium%3DSharebutton%26utm_campaign%3DDefualt&adjust_campaign=Sharebutton&adjust_deeplink=" + encodeURIComponent("viber://forward?text=" + encodeURIComponent(dataHref));
        }
        //hangouts
        else if(dataPage == 'hg'){
            locaiton.href = "https://plus.google.com/share?url="+dataHref;
        }
        //email
        else if(dataPage == 'em'){
            if(emailaddress)
                location.href="mailto:"+emailaddress + '&body='+dataHref;
        }



    });
})
