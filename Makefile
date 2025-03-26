start: backend/code/qq/__init__.py
	docker-compose up -d
shell: backend/code/qq/__init__.py
	docker-compose exec webapi bash
backend/code/qq/__init__.py:
	sudo mount -o bind /home/socek/projects/sapp/qq backend/code/qq
