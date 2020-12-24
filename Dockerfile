FROM mangadl/manga-py_base:1.0.2

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

RUN python3 -m pip install manga-py==1.25.0

RUN rm -rf /tmp/.P* /var/lib/apt/lists/*

USER $HOST_USER
WORKDIR $HOME

# docker run -it -v /tmp/destination:/home/manga mangadl/manga-py

ENTRYPOINT  ["manga-py"]
CMD ["manga-py", "--version"]
