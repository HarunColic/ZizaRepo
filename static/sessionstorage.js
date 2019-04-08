$('input').change((e)=>{
	sessionStorage.setItem(e.target.getAttribute('name'),e.target.value)
	localStorage.setItem(e.target.getAttribute('name'),e.target.value)
	//console.log(e.target.value);
})

$('select').change((e)=>{
	sessionStorage.setItem(e.target.getAttribute('name'),e.target.value)
	localStorage.setItem(e.target.getAttribute('name'),e.target.value)
})



/* var elements = document.getElementsByTagName('input');

    for (let i = 0; i < elements.length; i++) {

        var name = elements[i].getAttribute('name');

        elements[i].value = localStorage.getItem(name);
    }
*/
$(document).ready(()=>{
	$('input').not('input[type=hidden] input[type=file]').each((i,e)=>{
		if(sessionStorage.getItem(e.getAttribute('name')))
		e.value = sessionStorage.getItem(e.getAttribute('name'));
	});
	$('select').each((i,e)=>{
		if(sessionStorage.getItem(e.getAttribute('name')))
		e.value = sessionStorage.getItem(e.getAttribute('name'));
    });

	if(sessionStorage.getItem('desc'))list
	$('#editor-container').html(sessionStorage.getItem('desc'));

var quill = new Quill('#editor-container', {
	modules: {
		toolbar: [
		['bold', 'italic'],
		['link', 'blockquote', 'code-block'],
		[{ list: 'ordered' }, { list: 'bullet' }, 'image', 'video']
		]
	},
	placeholder: 'Unesite detaljan opis Vašeg oglasa...',
	theme: 'snow'
	});

	quill.clipboard.addMatcher(Node.ELEMENT_NODE, (node, delta) => {
	delta.ops = delta.ops.map(op => {
		return {
		insert: op.insert
		}
	})
	return delta
	});
	quill.on('editor-change', function(e) {
		if (e === 'text-change') {
			sessionStorage.setItem('desc',$('.ql-editor').html())
		}
	});
})

$(document).ready( function() {
    $(".ql-editor").attr('spellcheck',false);
    $('.ql-image').html('Postavi sliku').css('width', '90px').css('color', 'rgba(0,0,0,0.6)');
    $('.ql-video').html('Postavi video').css('width', '90px').css('color', 'rgba(0,0,0,0.6)');

});

let counter = 0;
    let lcounter = 0;
    let lcounter2 = 0;
    let url = location.href.split('?')[1];
     let fields = url.split('&');
     let selectedPage = 1;
    var options = {
  types: ['(cities)']
};
let initialize=false;

$(document).ready(function(){
     fields.forEach(element => {
        let temp=element.split('=');
        if(temp[1]){
            temp[1] = temp[1].replace(/\+/g,' ');
            temp[1]=decodeURIComponent(temp[1]);
             if(temp[0] != 'page'){
                $("input[type='text'][name='"+temp[0]+"']").val(temp[1]);
                $("input[type='checkbox'][name='"+temp[0]+"'][value='"+temp[1]+"']").prop('checked',true);
                $("select[name='"+temp[0]+"']").val(temp[1]);
                $("input[type='number'][name='"+temp[0]+"']").val(temp[1]);
			 }

		}

     });

 })