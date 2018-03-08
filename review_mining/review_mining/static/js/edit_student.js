function placeCaretAtEnd(el)
{
    el.focus();
    if (typeof window.getSelection != "undefined"
            && typeof document.createRange != "undefined")
    {
        var range = document.createRange();
        range.selectNodeContents(el);
        range.collapse(false);
        var sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
    }
    else if (typeof document.body.createTextRange != "undefined")
    {
        var textRange = document.body.createTextRange();
        textRange.moveToElementText(el);
        textRange.collapse(false);
        textRange.select();
    }
}
$(document).ready(function()
{
	var temp_data;
	var fetch_records = function()
	{
		var batch = $("#search_by_batch").val();
		var name = $("#search_by_name").val();
		var csrf = $("#csrf_token").find("input").val();

		$.ajax
		({
			type: "POST",
			url: "student/edit_student/",
			data: { batch: batch, name: name, csrfmiddlewaretoken: csrf },
			success: function(response)
			{
				$("#append_student_records").html(response);
				$(".select").select2
                ({
                    allowClear: true
                });
			}
		});
	}
	fetch_records();
	$("#search_by_batch").change(fetch_records);
	$("#search_by_name").keyup(fetch_records);
	

	$(document).on("mouseenter", ".data_grp", function()
	{
    	$(this).find(".edit_btn").show();
	});
	$(document).on("mouseleave", ".data_grp", function()
	{
		$(this).find(".edit_btn").hide();
	});
	
	$(document).on("click",".edit_btn",function()
	{
		content = $(this).parents(".data_grp").find(".data_div").find(".data");
		content.attr("contenteditable",true);
		content.focus();

		placeCaretAtEnd(content.get(0));
		temp_data = content.text();
	});
	$(document).on("blur",".data",function()
	{
		var rel = $(this).parents(".data_grp").attr('rel');
		var data = $(this).text().trim();
		var caller = $(this);
		var csrf = $("#csrf_token").find("input").val();
		var checker = /^\d+$/.test(data);

		if($(this).parents(".data_grp").find(".edit_btn").hasClass("sms_check"))
			sms_check = /^\d{10}$/.test(data);
		else
			sms_check = true

		if($(this).parents(".data_grp").find(".edit_btn").hasClass('check_num') && (checker == false || sms_check == false))
		{
			if(checker == false)
			{
				alert_content = "You can only use digits in this field!";
			}
			else
			{
				alert_content = "Enter exactly 10 digits";
			}
			$.alert
			({
			    title: 'Alert!',
			    content: alert_content,
			    closeIcon: true,
    			closeIconClass: 'glyphicon glyphicon-remove',
    			confirmButton: 'Okay',
    			confirmButtonClass: 'btn-danger',
    			confirm: function()
				{
					caller.text(temp_data);
					caller.parents(".data_grp").find(".edit_btn").trigger('click');
				},
				cancel: function()
				{
					caller.text(temp_data);
					caller.parents(".data_grp").find(".edit_btn").trigger('click');
				}
			});
			checker = sms_check = true;
			return;
		}
		else
		{
			$.ajax
			({
				type: "POST",
				url: "student/update_cell/",
				data: { cell: rel, data: data, csrfmiddlewaretoken: csrf},
				success: function()
				{
					caller.removeAttr("contenteditable");
				}
			});
		}
	});
	$(document).on("change",".batch_edit",function()
	{
		var rel = $(this).parents(".data_grp").attr('rel');
		var data = $(this).val();
		var caller = $(this);
		var csrf = $("#csrf_token").find("input").val();
		$.ajax
		({
			type: "POST",
			url: "student/update_cell/",
			data: { cell: rel, data: data, csrfmiddlewaretoken: csrf},
			success: function()
			{
				if(response=="false")
					alert("There was some problem updating the data.");
				else
				{
					caller.removeAttr("contenteditable");
				}
			}
		});
	});
	$(document).on("click",".full_edit_btn",function()
	{
		var rel = $(this).attr('rel');
		var csrf = $("#csrf_token").find("input").val();
		$.ajax
		({
			type: "GET",
			url: "student/edit_full_student/"+rel+"/",
			data: { csrfmiddlewaretoken: csrf },
			success: function(response)
			{
				$("#edit_content").html(response+'<script src="/static/js/add_student.js"></script>');
				$("#edit_content").find("form").attr('action','student/edit_full_student/'+rel+'/');
				$("#id_batch").css({'width': '110%',"padding": "0px"});
				$("#id_batch").select2
                ({
                    allowClear: true
                });
			}
		});
	});
	$(document).on("click",".delete_btn",function()
	{
		var rel = $(this).attr('rel');
		var csrf = $("#csrf_token").find("input").val();
		var caller = $(this).parents(".student_record");
		$.confirm
		({
			title: 'Are you sure?',
			content: "You won't be able to revert this action!" ,
			confirmButton: 'Delete',
			confirmButtonClass: 'btn-danger',
			cancelButton: 'Cancel',
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
					url: "student/delete_student/",
					data: { key: rel, csrfmiddlewaretoken: csrf },
					success: function()
					{
						caller.fadeOut("slow");
					}
				});
			},
			cancel: function()
			{
			    
			}
		});
	});
});