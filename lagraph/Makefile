wheel:
	python setup.py bdist_wheel

wheel_manylinux:
	docker build -t gb .
	docker create -it --name gb gb sh
	sleep 0.5
	docker cp gb:/home/app/dist/ ./dist/
	docker cp gb:/home/app/wheelhouse/ ./wheelhouse/
	docker rm gb