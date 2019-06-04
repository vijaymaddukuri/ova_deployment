FROM vijaymaddukuri/vijay

MAINTAINER vijaymaddukuri@yahoo.com

RUN yum_install curl epel-release java-1.8.0-openjdk-devel libxslt tar rpm-build \
 git perl-Git \
 && yum clean all

RUN echo "export JAVA_HOME=/usr/lib/jvm/java-1.8.0" >> /home/jenkins/.bashrc
RUN yum groupinstall -y 'development tools'
RUN yum install -y zlib-dev openssl-devel sqlite-devel bzip2-devel xz-libs

ENV APPLICATION_DIR="/srv/application"
# Install required packages
RUN yum update -y; yum clean all
RUN yum -y install wget
#PYTHON 3.2
RUN yum -y groupinstall "Development tools"
RUN yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel
RUN yum -y install python36
RUN yum -y install python36-devel
RUN yum -y install python36-setuptools
RUN ls -l /usr/lib/python3.6/
RUN echo $PATH
RUN cd /usr/lib/python3.6/site-packages/ && python3.6 easy_install.py -d  /usr/lib/python3.6/site-packages/ pip
RUN export PYTHONPATH=/usr/lib/python3.6/site-packages/


USER build
