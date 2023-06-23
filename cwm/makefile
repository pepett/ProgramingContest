all:
	sass --watch ./static/scss/:./static/css/
databasereset:
	del db.sqlite3
	del ./cwmapp/migrations/*.py
	type nul > ./cwmapp/migrations/__init__.py
	rd -rf __pycache__
	python manage.py makemigrations
	python manage.py migrate