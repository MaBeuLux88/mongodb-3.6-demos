FROM python:alpine3.6

ADD retryableWrites.py /
ADD requirements.txt /

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r ./requirements.txt

ENTRYPOINT ["python", "-u", "retryableWrites.py"]
