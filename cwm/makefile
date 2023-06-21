all:
	sass --watch ./static/scss/:./static/css/
databasereset:
	del db.sqlite3
	del ./cwmapp/migrations/*.py
	type nul > __init__.py
	rd -rf __pycache__
	django-admin makemigrations
	django-admin migrate