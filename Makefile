build:
	docker build -t websklad-be .

list:
	docker ps --all

dev:
	docker build -t websklad-be . && docker run -p 8000:8000 --rm --name Websklad-BE websklad-be

start:
	docker run -p 8000:8000 --rm --name Websklad-BE websklad-be