FROM python:alpine3.6

ADD causalConsistency.py /
ADD requirements.txt /

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r ./requirements.txt

# Here we insert some data
ENTRYPOINT ["python", "-u", "causalConsistency.py"]
