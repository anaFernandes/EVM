From ubuntu:16.04 

USER root

# Install Ubuntu updates
RUN apt-get update && apt-get upgrade -y
#RUN apt-get update && apt-get install -y  

#Create evm user
RUN groupadd -r -g 5000 evm && \
    useradd -mr -c "evm" -g 5000 -u 5000 evm

#RUN apt-get install -y  python-pip
RUN apt-get install python2.7 -y
RUN apt-get install python-pip -y


#Direitos da pasta app (quem é o dono e o que cada um pode fazer)
RUN mkdir -p /home/evm/app &&\
	chown 1000.5000 -R /home/evm/app &&\
	chmod -R 777 /home/evm/app

RUN pip install --upgrade pip &&\
	pip install virtualenv

RUN apt-get install python-scipy -y

RUN  apt-get install libmysqlclient-dev -y
USER evm

WORKDIR /home/evm

RUN virtualenv env &&\
	echo ". /home/evm/env/bin/activate" >> ~/.bashrc	

RUN . env/bin/activate &&\
	pip install numpy pymysql &&\ 
	pip install wheel matplotlib pandas &&\
	pip install -U scikit-learn &&\
	pip install scipy 

WORKDIR /home/evm/app
