FROM python:alpine3.14

RUN apk --update --upgrade add --no-cache gcc musl-dev linux-headers
RUN python -m pip install --upgrade pip
RUN pip3 install requests psutil click flask python_on_whales
COPY . .
COPY /templates /templates
COPY /static /static

CMD [ "python", "main.py" ]
