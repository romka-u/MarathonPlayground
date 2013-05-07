
page = """

<script type = "text/javascript" src="http://code.jquery.com/jquery-1.9.1.min.js"></script>
<script type = "text/javascript">
    $(document).ready(function()
    {{
        var id = window.setInterval(function() {{
            var jqxhr = $.ajax({{
                        url: "http://localhost:8051/submissions",
                        crossDomain: true}})
                    .done(function(data) {{
                              submissions = $("#submissions", '<div>' + data + '</div>')
                              $("#submissions").replaceWith(submissions)
                              imgs = $("img", '<div>' + data + '</div>')
                              if (imgs.length == 0) clearInterval(id);
                              //console.log("success " + submissions.html() );
                          }})
                    .fail(function() {{ console.log("error"); }})
                    .always(function() {{ }});

        }}, 3500);
    }});
</script>

<h1>Submissions page</h1><hr>
<form enctype="multipart/form-data" action="http://localhost:8051/submissions" method="post">
<p>{message}</p>
<p>Solution: <input type="file" name="file">Comment:<input type="text" name="comment"><input type="submit" value="Upload"></p>
</form>
<hr>
"""

