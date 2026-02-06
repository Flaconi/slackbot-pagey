FROM python:3.14-alpine3.23 AS builder

# Ensure pip, setuptools, wheel and build are available for building and installing the package
RUN set -eux \
    && python -m ensurepip --upgrade \
    && python -m pip install --no-cache-dir --upgrade pip setuptools wheel build

COPY ./ /data
RUN set -eux \
	&& cd /data \
	&& python -m build \
	&& python -m pip install --no-cache-dir dist/*.whl \
	\
	&& pagey --version | grep -E '^pagey.+?[.0-9]{5}' \
	\
	&& find /usr/lib/ -name '__pycache__' -print0 | xargs -0 -n1 rm -rf \
	&& find /usr/lib/ -name '*.pyc' -print0 | xargs -0 -n1 rm -rf


FROM python:3.14-alpine3.23 AS production
# https://github.com/opencontainers/image-spec/blob/master/annotations.md
#LABEL "org.opencontainers.image.created"=""
#LABEL "org.opencontainers.image.version"=""
#LABEL "org.opencontainers.image.revision"=""
LABEL "maintainer"="DevOps <devops@flaconi.de>"
LABEL "org.opencontainers.image.authors"="DevOps <devops@flaconi.de>"
LABEL "org.opencontainers.image.vendor"="flaconi"
LABEL "org.opencontainers.image.licenses"="MIT"
LABEL "org.opencontainers.image.url"="https://github.com/Flaconi/slackbot-pagey"
LABEL "org.opencontainers.image.documentation"="https://github.com/Flaconi/slackbot-pagey"
LABEL "org.opencontainers.image.source"="https://github.com/Flaconi/slackbot-pagey"
LABEL "org.opencontainers.image.ref.name"="pagey ${VERSION}"
LABEL "org.opencontainers.image.title"="pagey ${VERSION}"
LABEL "org.opencontainers.image.description"="pagey ${VERSION}"

RUN set -eux \
	&& addgroup -g 1000 pagey \
	&& adduser -h /home/pagey -s /bin/sh -u 1000 -G pagey -D pagey

RUN set -eux \
	&& ln -sf /usr/local/bin/python3 /usr/bin/python \
	&& ln -sf /usr/local/bin/python3 /usr/local/bin/python \
	\
	&& find /usr/lib/ -name '*.pyc' -print0 | xargs -0 -n1 rm -f \
	&& find /usr/lib/ -name '__pycache__' -print0 | xargs -0 -n1 rm -rf

COPY --from=builder /usr/local/lib/python3.14/site-packages/ /usr/local/lib/python3.14/site-packages/
COPY --from=builder /usr/local/bin/pagey /usr/local/bin/pagey

USER pagey
ENTRYPOINT ["pagey"]
