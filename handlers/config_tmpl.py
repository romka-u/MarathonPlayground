
page = """
<h1>Config page</h1>
<hr>
<form action="http://localhost:8051/config" method="get">
<p>Test seeds:</p>
<p><textarea name="seeds" rows=20 cols=12>
{seeds}
</textarea></p>
<p><input type="submit" value="Update"></p>
</form>
"""