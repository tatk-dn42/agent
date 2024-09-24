FROM python:3.12-bookworm

WORKDIR /app

RUN useradd -ms /bin/bash app

RUN apt-get update -y \
 && apt-get install --no-install-recommends -y iproute2=6.1.0-3 bird2=2.0.12-7 wireguard=1.0.20210914-1 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* \

RUN echo 'PUBLIC_KEY' > /etc/wireguard/publickey

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

USER app

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

EXPOSE 5000

HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://localhost:5000 || exit 1