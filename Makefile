migrate:
	@alembic upgrade head

up:
	@alembic upgrade head
	@echo "starting"
	@gunicorn app.patched:app --worker-class gevent -w 1 -b 0.0.0.0:8000 

test:
	@alembic upgrade head
	@clear
	@pytest  --durations=0 -v --cov=app

format:
	@isort app/
	@isort tests/
	@black app/
	@black tests/

doc:
	@python create_doc.py > my_website_be.html
