FROM python:3.11-alpine

WORKDIR /app

COPY attackers/mqtt-lwt-abuse/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY attackers/mqtt-lwt-abuse/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

COPY attackers/mqtt-lwt-abuse/mqtt-lwt-abuse.py /app/mqtt-lwt-abuse.py

ENV TARGET_HOST=localhost

ENTRYPOINT ["/app/entrypoint.sh"]
