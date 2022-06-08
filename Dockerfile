FROM mcr.microsoft.com/playwright/python:v1.22.0-focal

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/
RUN playwright install
RUN pip install --no-cache-dir -r requirements.txt

CMD ["pytest", "tests/"]