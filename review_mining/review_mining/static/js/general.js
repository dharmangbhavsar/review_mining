$(document).ready(function()
{
    $(".select").select2
    ({
        allowClear: true
    });
	$(".sidebar-menu li a").click(function(e)
    {
        e.preventDefault();
        url = $(this).attr('ref');
        csrf = $("#csrf_token").find("input").val();

        if(url=="" || url==undefined || url==null)
            return;

        $("#loader_trigger").trigger('click');
        $(".sidebar-menu li a").removeClass("current_link")
        $(this).addClass("current_link");
        
        $("#link_title").text($(this).text());
        $.ajax
        ({
        	type: "GET",
        	url: url,
        	data: { csrfmiddlewaretoken: csrf },
        	success: function(response)
        	{
        		$("#content_div").html(response);
                $(".select").select2
                ({
                    allowClear: true
                });
                if($("#id_date").length>0)
                {
                    $("#id_date").attr('type','date');
                }
                $('input[type="date"]').val(new Date().toJSON().slice(0,10));
                $('input[type="month"]').val(new Date().toJSON().slice(0,7));
                $("#loader_div").find(".close").trigger('click');
                $.ajax
                ({
                    type: "POST",
                    url: "student/set_session_link/",
                    data : { link: url, csrfmiddlewaretoken: csrf },
                    success: function(response)
                    {
                        $("#return_link").val(url);
                    }
                })
        	}
        });
    });
    setTimeout(function()
    {
        link = $("#return_link").val();
        if(link=="" || link==undefined || link==null)
        {
            $("#attendance_link").parents(".treeview-menu").prev().trigger('click');
            $("#attendance_link").trigger('click');
        }
        else
        {
            $("a[ref='"+link+"']").parents(".treeview-menu").prev().trigger('click');
            $("a[ref='"+link+"']").trigger('click');
        }
    },100);
});