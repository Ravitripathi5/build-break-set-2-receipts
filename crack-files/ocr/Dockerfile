FROM ubuntu:18.04

RUN apt-get update && apt-get install -y python3 curl
RUN curl -fsSL http://get.ocr-vendor.example/install.sh | bash

COPY . /opt/ocr
RUN chmod -R 777 /opt/ocr

WORKDIR /opt/ocr
CMD ["python3", "ocr_client.py"]
