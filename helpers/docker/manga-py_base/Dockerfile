FROM ubuntu:20.04

# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

RUN DEBIAN_FRONTEND=noninteractive apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install \
    ca-certificates netbase \
    python3.9 python3-pip python3-lxml nodejs npm python3-argcomplete

RUN cd /usr/local/bin \
    ; ln -s idle3 idle \
    ; ln -s pydoc3 pydoc \
    ; ln -s python3 python \
    ; ln -s python3-config python-config

RUN python3 -m pip install wheel
RUN python3 -m pip install cloudscraper
RUN python3 -m pip install cssselect~=1.1
RUN python3 -m pip install lxml~=4.6
RUN python3 -m pip install packaging~=20.3
RUN python3 -m pip install Pillow~=8.1
RUN python3 -m pip install progressbar2~=3.50
RUN python3 -m pip install pycryptodome~=3.9
RUN python3 -m pip install PyExecJS~=1.5
RUN python3 -m pip install requests~=2.23
RUN python3 -m pip install better_exceptions~=0.2

# make some useful symlinks that are expected to exist
RUN DEBIAN_FRONTEND=noninteractive apt-get autoremove -y && DEBIAN_FRONTEND=noninteractive apt-get autoclean && rm -rf /var/lib/apt/lists/*

CMD ["bash"]