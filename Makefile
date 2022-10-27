SHELL = /bin/bash
.DEFAULT_GOAL := serve

serve:
	pipenv run gunicorn flask_frontend:app

dev:
	pipenv run gunicorn flask_frontend:app --reload

clean:
	rm -rf static/*
	touch static/.gitkeep

batch:
	pipenv run python3 batch-process.py

