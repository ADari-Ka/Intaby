FROM python:3.9.7

COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY ./ ./
EXPOSE 8080
ENTRYPOINT ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=8888"]

ENV PYTHONPATH=/web-app:/web-app/adapters:/web-app/entrypoints:/web-app/domain:/web-app/service_layer:$PYTHONPATH
