FROM arm32v7/ubuntu:latest
RUN mkdir -p /usr/docker_campi4
RUN apt update
RUN export TERM=xterm
RUN apt install git -y
RUN apt install python-pip python-setuptools python-wheel python-pygame -qy --no-install-recommends
RUN cd /usr/docker_campi4/
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN cd /usr/docker_campi4/;git clone https://github.com/agrasagar/campi4.git
RUN cd /usr/docker_campi4/campi4
WORKDIR /usr/docker_campi4/campi4
EXPOSE 5994/tcp
ENV NAME campi4
ENTRYPOINT ["python", "app.py", "-p", "5994"]

