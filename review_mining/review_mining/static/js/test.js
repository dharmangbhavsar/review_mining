$(document).ready(function()
{
	$(document).on("change","#test_batch",function()
	{
		var batch = $("#test_batch").val();
		var csrf_token = $("#csrf_token").find("input").val();
		$.ajax
		({
		// Check for batch id instead of standard
			type: "POST",
			url: "student/get_test_students/",
			data: { batch: batch, csrfmiddlewaretoken: csrf_token },
			success: function(response)
			{
				$("#test_table").html(response);
			},
			error: function()
			{
				response = '[{"fname":"Vismay","lname":"Golwala","contact":"9898989898"},{"fname":"Umang","lname":"Jain","contact":"4545454545"},{"fname":"Vortex","lname":"Wow","contact":"7373737373"},{"fname":"Argon","lname":"Wow","contact":"1212121212"},{"fname":"Focus","lname":"Wow","contact":"4747474747"}]';
				var obj = JSON.parse(response);
				document.getElementById("attendance_table").innerHTML = "";
				$.each(obj, function(key, value)
				{
				    document.getElementById("attendance_table").innerHTML += '<div class="col-sm-12"><div class="col-sm-1">'+key+'</div><div class="col-sm-2">'+value.fname+'</div><div class="col-sm-2">'+value.lname+'</div><div class="col-sm-2">'+value.contact+'</div><div class="col-sm-4"><div class="col-sm-6"><label class="radio-inline"><input type="radio" class="attendance_radio" name="optradio_'+key+'" checked> Present</label></div><div class="col-sm-6"><label class="radio-inline"><input type="radio" class="attendance_radio" name="optradio_'+key+'"> Absent</label></div></div><div class="clearfix"></div><br/>';
				});
				document.getElementById("attendance_table").innerHTML += '<div class="col-sm-12"><button class="btn btn-success btn-lg">Save</button></div>'
			}
		})
	});
});