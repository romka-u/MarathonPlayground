
page = """
<h1>Submissions page</h1>
<hr>
<form enctype="multipart/form-data" action="http://localhost:8051/submissions" method="post">
<p>{message}</p>
<p>Solution: <input type="file" name="file">Comment:<input type="text" name="comment"><input type="submit" value="Upload"></p>
</form>
<hr>
"""
