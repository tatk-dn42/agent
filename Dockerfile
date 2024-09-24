FROM python:3.12-bookworm

WORKDIR /app

RUN apt-get update -y && apt-get install -y iproute2 bird2 wireguard
RUN echo 'PUBLIC_KEY' > /etc/wireguard/publickey

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

EXPOSE 5000