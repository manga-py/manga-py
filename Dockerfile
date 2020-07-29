FROM ubuntu:18.04

# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

# runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
                ca-certificates \
                netbase \
        && rm -rf /var/lib/apt/lists/*

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

RUN DEBIAN_FRONTEND=noninteractive apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install \
    libxml2-dev libxslt1-dev python3.6 python3-pip python3-lxml python3-pil \
    python3-pil.imagetk nodejs npm python3-argcomplete libjpeg-dev zlib1g-dev

RUN DEBIAN_FRONTEND=noninteractive apt-get autoremove -y && DEBIAN_FRONTEND=noninteractive apt-get autoclean

# make some useful symlinks that are expected to exist
RUN cd /usr/local/bin \
    ; ln -s idle3 idle \
    ; ln -s pydoc3 pydoc \
    ; ln -s python3 python \
    ; ln -s python3-config python-config

RUN python3 -m pip install manga-py -U --no-cache-dir

RUN echo 'Manga-py version: '; \
    manga-py --version; \
    rm -rf /tmp/.P*

USER $HOST_USER
WORKDIR $HOME

# docker run -it -v /tmp/destination:/home/manga mangadl/manga-py

ENTRYPOINT  ["manga-py"]
CMD ["manga-py", "--version"]
