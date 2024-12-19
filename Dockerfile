# checkov:skip=CKV_DOCKER_3:Running as root required for raw net access
FROM python:3.12-bookworm

WORKDIR /app

RUN apt-get update -y \
 && apt-get install --no-install-recommends -y iproute2=6.1.0-3 bird2=2.0.12-7 wireguard=1.0.20210914-1 iputils-ping=3:20221126-1+deb12u1 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

RUN mkdir -p /run/bird \
  && mkdir /peers \
  && chown -R bird: /peers \
  && chmod g+w /peers

COPY bird_config/* /etc/bird

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

EXPOSE 5000

HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://localhost:5000/api/meta/info || exit 1