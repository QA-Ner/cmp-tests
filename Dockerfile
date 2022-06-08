FROM mcr.microsoft.com/playwright/python:v1.22.0-focal

RUN apt-get update  -y; apt-get install -y vim
RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/

RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install

EXPOSE 64520

CMD ["pytest", "tests/", "--alluredir=reports"]
#CMD ["allure", "serve", "reports/"]
