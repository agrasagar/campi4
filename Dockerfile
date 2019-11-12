FROM arm32v7/ubuntu:latest
WORKDIR /campi4
ADD . /campi4
RUN apt update
RUN apt install python-pip python-setuptools python-wheel python-pygame -qy --no-install-recommends
RUN pip install -r requirements.txt
EXPOSE 5994/udp
EXPOSE 5994/tcp
ENV NAME campi4
ENTRYPOINT ["python", "app.py", "-p", "5994"]

