$(document).ready(function()
{
	$(".batch_delete_btn").click(function()
	{
		var batch_pk = $(this).attr('rel');
		var csrf_token = $("#csrf_token").find("input").val();
		var caller = $(this).parents(".batch_row");

		$.confirm
		({
			title: 'Are you sure?',
			content: "You won't be able to revert this action!" ,
			confirmButton: 'Delete',
    		cancelButton: 'Cancel',
			confirmButtonClass: 'btn-danger',
    		cancelButtonClass: 'btn-info',
    		closeIcon: true,
    		closeIconClass: 'glyphicon glyphicon-remove',
    		theme: 'material',
    		backgroundDismiss: true,
			confirm: function()
			{
				$.ajax
				({
					type: "POST",
					url: "student/delete_batch/",
					data: { batch_pk: batch_pk, csrfmiddlewaretoken: csrf_token },
					success: function(response)
					{
						caller.fadeOut("slow");
					},
					error: function(response)
					{
						alert("Oops, this batch is bounded to some student model; Cannot delete!");
					}
				});
			},
			cancel: function()
			{
			    
			}
		});
	});
	$(".board_delete_btn").click(function()
	{
		var board_pk = $(this).attr('rel');
		var csrf_token = $("#csrf_token").find("input").val();
		var caller = $(this).parents(".board_row");

		$.confirm
		({
			title: 'Are you sure?',
			content: "You won't be able to revert this action!" ,
			confirmButton: 'Delete',
    		cancelButton: 'Cancel',
			confirmButtonClass: 'btn-danger',
    		cancelButtonClass: 'btn-info',
    		closeIcon: true,
    		closeIconClass: 'glyphicon glyphicon-remove',
    		theme: 'material',
    		backgroundDismiss: true,
			confirm: function()
			{
				$.ajax
				({
					type: "POST",
					url: "student/delete_board/",
					data: { board_pk: board_pk, csrfmiddlewaretoken: csrf_token },
					success: function(response)
					{
						caller.fadeOut("slow");
					},
					error: function(response)
					{
						alert("Oops, this board is bounded to some student model; Cannot delete!");
					}
				});
			},
			cancel: function()
			{
			    
			}
		});
	});
	$(".standard_delete_btn").click(function()
	{
		var standard_pk = $(this).attr('rel');
		var csrf_token = $("#csrf_token").find("input").val();
		var caller = $(this).parents(".standard_row");

		$.confirm
		({
			title: 'Are you sure?',
			content: "You won't be able to revert this action!" ,
			confirmButton: 'Delete',
    		cancelButton: 'Cancel',
			confirmButtonClass: 'btn-danger',
    		cancelButtonClass: 'btn-info',
    		closeIcon: true,
    		closeIconClass: 'glyphicon glyphicon-remove',
    		theme: 'material',
    		backgroundDismiss: true,
			confirm: function()
			{
				$.ajax
				({
					type: "POST",
					url: "student/delete_standard/",
					data: { standard_pk: standard_pk, csrfmiddlewaretoken: csrf_token },
					success: function(response)
					{
						caller.fadeOut("slow");
					},
					error: function(response)
					{
						alert("Oops, this standard is bounded to some student model; Cannot delete!");
					}
				});
			},
			cancel: function()
			{
			    
			}
		});
	});
});