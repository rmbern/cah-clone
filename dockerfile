FROM python:3.5-stretch

WORKDIR /

COPY . /

RUN pip install dist/cah_clone-0.0.1-py3-none-any.whl

EXPOSE 5000

CMD uwsgi --socket 0.0.0.0:5000 --protocol=http --wsgi-file cah.py --callable app
