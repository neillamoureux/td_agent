
# Simple use
# docker run -d -v \
# /path/to/fluentdconfdir:/etc/fluentd image/name

# Bionic Beaver
FROM ubuntu:18.04

# environment
ENV DEBIAN_FRONTEND noninteractive

# update
RUN apt-get update && apt-get -y upgrade

# ruby related packages for td-agent
RUN apt-get -y install curl libcurl4-openssl-dev ruby ruby-dev make gnupg2

# install fluentd td-agent
# td-agent 4
# RUN curl -L https://toolbelt.treasuredata.com/sh/install-ubuntu-bionic-td-agent4.sh | sh
# From https://toolbelt.treasuredata.com/sh/install-ubuntu-bionic-td-agent4.sh

ADD ./install.sh ./install.sh
RUN ./install.sh

# clean cache files
RUN apt-get clean && rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*

# install fluentd plugins
# RUN /opt/td-agent/embedded/bin/fluent-gem install --no-ri --no-rdoc \
#     fluent-plugin-elasticsearch \
#     fluent-plugin-record-modifier \
#     fluent-plugin-exclude-filter


# add conf
ADD ./etc/fluentd /etc/fluentd

# CMD /etc/init.d/td-agent stop && /opt/td-agent/embedded/bin/fluentd -c /etc/fluentd/fluent.conf
CMD /opt/td-agent/bin/fluentd
