FROM balenalib/rpi-raspbian:latest
#FROM arm32v7/ubuntu:latest
RUN mkdir -p /usr/docker_campi4
RUN apt update
RUN apt install git -y
RUN apt install python3-pip python3-setuptools python3-wheel python3-pygame -qy --no-install-recommends
RUN cd /usr/docker_campi4/
COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN cd /usr/docker_campi4/;git clone https://github.com/agrasagar/campi4.git
RUN cd /usr/docker_campi4/campi4
WORKDIR /usr/docker_campi4/campi4
EXPOSE 5994/tcp
ENV NAME campi4
RUN export TERM=xterm
ENTRYPOINT ["python3", "app.py", "-p", "5994"]

