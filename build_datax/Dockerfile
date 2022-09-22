FROM openjdk:8-alpine

MAINTAINER chq

RUN sed -i 's/http\:\/\/dl-cdn.alpinelinux.org/https\:\/\/mirrors.ustc.edu.cn/g' /etc/apk/repositories

RUN apk add --update --no-cache openssh python2 && \
    echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config && \
    echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && \
    echo -n 'root:zuY4Pai#' | chpasswd

# 添加并解压datax文件到/opt/local目录
ADD datax.tar.gz /opt/

VOLUME /opt/datax
# 设置运行的工作目录，可不添加,运行中使用 docker -w 指定
WORKDIR /opt/datax
COPY ./scripts/entrypoint.sh /
RUN chmod -R +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
