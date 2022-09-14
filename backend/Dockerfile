FROM python:3
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /usr/src/backend
COPY . .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
CMD ["bash", "entrypoint.sh"]
