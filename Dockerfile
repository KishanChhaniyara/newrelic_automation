FROM python:3.11.1
RUN echo $NRPYTHON

RUN apt-get update && apt-get -y install cron vim
WORKDIR /app
COPY requirement.txt /app/requirement.txt
COPY license.py /app/license.py
COPY nerdgraph_nrql.py /app/nerdgraph_nrql.py
COPY nrql.py /app/nrql.py

COPY client_secret.json /app/client_secret.json
RUN  pip3 install -r requirement.txt


RUN crontab -l | { cat; echo "29 18 * * * /usr/local/bin/python3 /app/nerdgraph_nrql.py"; } | crontab -
RUN crontab -l | { cat; echo "30 18 * * * /usr/local/bin/python3 /app/nrql.py"; } | crontab -
RUN touch /var/log/cron.log

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log

