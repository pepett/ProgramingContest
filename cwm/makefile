sassbuild:
	sass --watch ./static/scss/:./static/css/
re:
	del db.sqlite3
	rmdir /s /q .\$(app)\migrations\__pycache__
	del .\$(app)\migrations\*.py
	type nul >.\$(app)\migrations\__init__.py
	echo 'success!'
cr:
	python manage.py makemigrations
	python manage.py migrate
se:
	python manage.py runserver