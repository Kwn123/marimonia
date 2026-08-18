FROM python:3.12-slim

WORKDIR /app

COPY requirements-completo.txt .
RUN pip install --no-cache-dir -r requirements-completo.txt

COPY . .

RUN mkdir -p instance app/static/images/productos app/static/images/categorias

EXPOSE 5000

CMD ["python", "run.py"]
