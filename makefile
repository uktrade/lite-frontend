
clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

run_caseworker:
	PIPENV_DOTENV_LOCATION=caseworker.env pipenv run ./manage.py runserver localhost:8200

run_exporter:
	PIPENV_DOTENV_LOCATION=exporter.env pipenv run ./manage.py runserver localhost:8300

secrets:
	cp example.caseworker.env caseworker.env
	cp example.exporter.env exporter.env
