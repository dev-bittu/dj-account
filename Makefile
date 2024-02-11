.PHONY: *

migrate:
	python manage.py makemigrations
	python manage.py migrate

superuser:
	python manage.py createsuperuser

setup:
	pip install -r requirements.txt
	@make migrate
	@make superuser

run:
	python manage.py runserver

test:
	python manage.py test

push:
	git push -u origin main
