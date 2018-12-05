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
		console.log(e);
	});
	$('select').each((i,e)=>{
		if(sessionStorage.getItem(e.getAttribute('name')))
		e.value = sessionStorage.getItem(e.getAttribute('name'));
    });

	if(sessionStorage.getItem('desc'))
	$('#editor-container').html(sessionStorage.getItem('desc'));

var quill = new Quill('#editor-container', {
	modules: {
		toolbar: [
		['bold', 'italic'],
		['link', 'blockquote', 'code-block', 'image'],
		[{ list: 'ordered' }, { list: 'bullet' }]
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