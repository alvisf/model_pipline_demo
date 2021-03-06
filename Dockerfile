FROM ubuntu:20.04
LABEL maintainer="Alvis F" \
    name="alvisf" \
    version="0.0.2"
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get -y install python3 && \
    apt-get install -y python3-pip
COPY . /code/
RUN pip3 install -r /code/pdf-classification/requirements.txt
RUN apt-get install -y poppler-utils
RUN apt-get install -y tesseract-ocr


EXPOSE 5001
WORKDIR "/code/pdf-classification/"
# ENTRYPOINT ["python3"]
# CMD ["app.py"]