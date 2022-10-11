SHELL = /bin/bash
.DEFAULT_GOAL := serve

serve:
	gunicorn flask_frontend:app

dev:
	gunicorn flask_frontend:app --reload

clean:
	rm -rf static/*
	touch static/.gitkeep
