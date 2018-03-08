$(document).ready(function()
{
	$("#add_student_form, #edit_full_form").validate(
	{
		rules:
		{
			name: "required",
			batch: "required",
			school: "required",
			father_name: "required",
			father_mob:
			{
				required: true,
				digits: true,
				minlength: 10,
				maxlength: 10,
			},
			mother_name: "required",
			mother_mob:
			{
				required: true,
				digits: true,
				minlength: 10,
				maxlength: 10,
			},
			sms_mob:
			{
				required: true,
				digits: true,
				minlength: 10,
				maxlength: 10,
			},
			total_fees:
			{
				required: true,
				number: true,
			}
		},
		messages:
		{
			name: "Please enter student's name",
			batch: "Please select the batch. (You can create a new batch under 'Manage Batch' section)",
			school: "Please enter the school name",
			father_name: "Please enter father's name",
			father_mob:
			{
				required: "Please enter father's contact number",
				digits: "Mobile number should only have digits",
				minlength: "Enter exactly 10 digits",
				maxlength: "Enter exactly 10 digits",
			},
			mother_name: "Please enter mother's name",
			mother_mob:
			{
				required: "Please enter mother's contact number",
				digits: "Mobile number should only have digits",
				minlength: "Enter exactly 10 digits",
				maxlength: "Enter exactly 10 digits",
			},
			sms_mob:
			{
				required: "Please enter sms contact number",
				digits: "Mobile number should only have digits",
				minlength: "Enter exactly 10 digits",
				maxlength: "Enter exactly 10 digits",
			},
			total_fees:
			{
				required: "Please enter student's total fees",
				number: "Fees should only be a number"
			},
		}
	});
});