SHELL := /bin/bash
.ONESHELL:

mongo:
	# For windows users,
        # mongod.exe --dbpath="c:\data\db"

minio:
	# For windows users,
	# minio.exe server D:\path\to\plotly_graphene\minio

frontend:
	cd client
	npm install --silent
	npm install react-scripts@3.0.1 -g --silent
	npm start

backend:
	cd server
	source bin/activate
	pip install -r requirements.txt
	uvicorn main:app --host 0.0.0.0 --port 8000 --reload
