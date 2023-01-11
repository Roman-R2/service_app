docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-build-up:
	docker-compose up -d --build

docker-down:
	docker-compose down --remove-orphans

docker-down-remove-volumes:
	docker-compose down -v --remove-orphans

docker-logs:
	docker-compose -f docker-compose.yml logs -f

docker-logs-web-app:
	docker-compose -f docker-compose.yml logs web-app -f
# --------------------------------------------

# --- Django section ----------------------
migrate:
	docker-compose run --rm web-app sh -c "python manage.py migrate"

makemigrations:
	docker-compose run --rm web-app sh -c "python manage.py makemigrations"

createsuperuser:
	docker-compose run --rm web-app sh -c "python manage.py createsuperuser"
# --------------------------------------------