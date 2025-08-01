# Dockerfile for Flask application
FROM python:3.12-bookworm

WORKDIR /app
COPY ./flaskapp/ /app/

# security - criar usuário apenas se não for Windows
RUN if [ "$(uname)" != "MINGW64_NT" ]; then \
        addgroup --system appgroup && \
        adduser --system --ingroup appgroup appuser; \
    fi

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

# Create directories with broad permissions
RUN mkdir -p /app/fotos /app/thumbs /app/zips && \
    chmod -R 777 /app/fotos /app/thumbs /app/zips

# Only switch to appuser if it exists (Linux)
RUN if id appuser >/dev/null 2>&1; then \
        chown -R appuser:appgroup /app/fotos /app/thumbs /app/zips && \
        echo "USER appuser" > /tmp/user_cmd; \
    else \
        echo "# No user switch needed" > /tmp/user_cmd; \
    fi

# Execute the user switch command if needed
RUN cat /tmp/user_cmd > /tmp/user_switch.sh && chmod +x /tmp/user_switch.sh
RUN if grep -q "USER" /tmp/user_cmd; then /tmp/user_switch.sh; fi

CMD ["python", "app.py"]
