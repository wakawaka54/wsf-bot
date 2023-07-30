FROM mcr.microsoft.com/playwright/python:v1.35.0-jammy

WORKDIR /usr/bot

COPY . .

RUN pip install virtualenv && \
    virtualenv venv && \
    . venv/bin/activate && \
    pip install playwright==1.35.0 && \
    pip install -r requirements.txt

ENTRYPOINT [ "/bin/bash", "entrypoint.sh" ]