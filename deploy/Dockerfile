FROM python:3

#ADD build/requirements.txt /usr/local/ and install packages
ADD build/* /usr/local/.
RUN ls -la /usr/local/
RUN pip3 install -r /usr/local/requirements.txt

WORKDIR /usr/local