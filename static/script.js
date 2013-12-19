
$(document).ready(function() {

 	drawTodos();

 	//on form submit create a new todo and add to the todos list
 	$('#todoForm button').click(function() {
 		var title = $('#title').val();
 		if (!title) {
 			return false;
 		}
 		createTodo(title);
 		$('#title').val('');
 	});

 	//on click of delete link, remove todo from list
 	$('#todos').on('click', '.todo a.delete', function() {
 		deleteTodo($(this).parent().attr('id'));
 		return false;
 	});

 	//on change of checkbox status, toggle whether the todo is marked complete
 	$('#todos').on('click', '.todo input[type="checkbox"]', function() {

 		var isChecked = $(this).prop('checked');
 		var id = $(this).parent().attr('id');

 		$.ajax({
            url: '/todos/' + id,
            type: 'post',
            data: {
                done: isChecked ? 1 : 0
            }, 
            success: function() {
                drawTodos();
            }
        });
		
	
 	});

});

function createTodo(text) {
    var d = {
       title: text,
       done: 0
    };
	$.ajax({
        url: '/todos',
        type: 'post',
        data: d,
        success: function(data) {
            //$('#todos').append(buildTodo(d.id = data.id));
            drawTodos();
        }
    });
}

//remove a todo from the list
function deleteTodo(id) {
	$.ajax({
        url: '/todos/' + id,
        type: 'delete',
        success: function() {
            $('#' + id).remove();
        }
    });
	
}

//repopulate the todos div based on the current list
function drawTodos() {

    $.getJSON('/todos', function(todos) {
        $('#todos').empty();
        if (todos.length > 0) {
            $.each(todos, function(index, item) {
                el = buildTodo(item);
                $('#todos').append(el);
            });
        } else {
            $('#todos').append("<div class='message'>There's nothing to do!</div>");
        }
        
    });
}

function buildTodo(item) {
    var checked = item.done == 1 ? 'checked' : '';

    var el = $('<div class="todo" id="' + item.id + 
        '"><span class="title">' + item.title + 
        '</span><input type="checkbox" ' + checked + 
        '><a href="#" class="delete">Remove</a></div>');

    if (item.done == 1) {
        el.addClass('completed');
    }
    
    return el;
}
