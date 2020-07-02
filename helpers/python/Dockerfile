FROM python:3.7.8-stretch

ARG HOST_UID=1000
ARG HOST_GID=1000
ARG HOST_USER=manga
ARG HOST_GROUP=manga
ARG HOME='/home/manga'

RUN groupadd -g $HOST_GID $HOST_GROUP \
    && groupadd sudonopswd \
    && useradd -m -l -g $HOST_GROUP -u $HOST_UID $HOST_USER

RUN mkdir $HOME -p; \
    chown $HOST_USER:$HOST_GROUP $HOME

RUN touch $HOME/.bashrc; \
    mkdir $HOME/Manga; \
    chown $HOST_USER:$HOST_GROUP $HOME/.bashrc; \
    chown $HOST_USER:$HOST_GROUP $HOME/Manga

RUN python3 --version
RUN python3 -mpip install manga-py -U --no-cache-dir \
# Because it requires gcc
        && python3 -mpip install manga-py -U --no-cache-dir \
        && curl -sL https://deb.nodesource.com/setup_12.x | bash - \
	&& apt-get install -y nodejs

USER $HOST_USER
WORKDIR $HOME

RUN echo 'Manga-py version: '; \
    manga-py --version; \
    rm -rf /tmp/.P*

# docker run -it -v /tmp/destination:/home/manga mangadl/manga-py

CMD ["bash"]
