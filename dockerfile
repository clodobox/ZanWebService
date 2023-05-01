FROM ubuntu:23.04
RUN apt-get update --fix-missing && \
    apt-get install -y software-properties-common wget apt-utils && \
    rm -rf /var/lib/apt/lists/*  && \
    wget -O - http://debian.drdteam.org/drdteam.gpg | apt-key add - && \
    add-apt-repository 'deb http://debian.drdteam.org/ stable multiverse' && \
    apt update && \
    apt install -y python3 python3-werkzeug python3-flask zandronum-server && \
    rm -rf /var/lib/apt/lists/* && \
    apt remove -y software-properties-common wget apt-utils
    apt clean
RUN add-apt-repository 'deb http://debian.drdteam.org/ stable multiverse'
RUN apt-get -y autoclean
COPY app.py app.py
#RUN useradd -ms /bin/bash -u 1026 -g 100 user123
#USER user123
ENTRYPOINT ["/bin/python3"]