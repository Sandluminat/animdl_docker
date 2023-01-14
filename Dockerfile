FROM python:3.10.6

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./subprocess_test.py /code/
COPY ./runner.py /code/

EXPOSE 8501

CMD ["streamlit", "run", "subprocess_test.py", "--server.port=8501", "--server.address=0.0.0.0"]