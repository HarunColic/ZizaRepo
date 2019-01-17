$('input').change((e)=>{
	sessionStorage.setItem(e.target.getAttribute('name'),e.target.value)
	//console.log(e.target.value);
})

$('select').change((e)=>{
	sessionStorage.setItem(e.target.getAttribute('name'),e.target.value)
})

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