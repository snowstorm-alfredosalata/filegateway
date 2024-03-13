FROM debian:bookworm-slim
LABEL AUTHOR="as@salata.ovh"

ENV LANG C.UTF-8

RUN apt update \
    && apt install -y --no-install-recommends \
        python3-dev \
        python3-pip

COPY ./dist /dist

# Set permissions and Mount /var/lib/odoo to allow restoring filestore and /mnt/extra-addons for users addons
RUN mkdir /dist/filegateway && \
    tar -xzvf $(ls /dist/*.tar.gz | head -1) -C /dist/filegateway --strip-components=1 && \
    pip3 install /dist/filegateway --break-system-packages

EXPOSE 5000

ENTRYPOINT ["filegateway"]