# Dockerfile for Flask application
FROM python:3.12-bookworm

WORKDIR /app
COPY ./flaskapp/ /app/

# security - criar usuário apenas se não for Windows
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser

RUN apt update -y && \
    apt upgrade -y && \
    apt install -y nano dos2unix cron && \
    apt autoclean -y && \
    apt autoremove -y

RUN apt update -y && \
    apt install -y libgl1-mesa-glx && \
    apt autoclean -y && \
    apt autoremove -y

RUN dos2unix -i -o ./*.sh && \
    chmod +x ./*.sh

RUN python -m pip install pip --upgrade
RUN python -m pip install -r requirements.txt --no-cache-dir

# Não criar diretórios aqui - serão criados pelo código Python
# com as permissões corretas após o volume ser montado

# Dar ownership de todo /app para appuser
RUN chown -R appuser:appgroup /app

USER appuser

CMD ["python", "app.py"]
