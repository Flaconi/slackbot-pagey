FROM python:3.12-alpine3.20 as builder

COPY ./ /data
RUN set -eux \
	&& cd /data \
	&& python setup.py install \
	\
	&& pagey --version | grep -E '^pagey.+?[.0-9]{5}' \
	\
	&& find /usr/lib/ -name '__pycache__' -print0 | xargs -0 -n1 rm -rf \
	&& find /usr/lib/ -name '*.pyc' -print0 | xargs -0 -n1 rm -rf


# 3.20 uses Python 3.12 as default
FROM alpine:3.20 as production
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
	&& apk add --no-cache python3 \
	&& ln -sf /usr/bin/python3 /usr/bin/python \
	&& ln -sf /usr/bin/python3 /usr/local/bin/python \
	\
	&& find /usr/lib/ -name '*.pyc' -print0 | xargs -0 -n1 rm -f \
	&& find /usr/lib/ -name '__pycache__' -print0 | xargs -0 -n1 rm -rf

COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/pagey /usr/bin/pagey

USER pagey
ENTRYPOINT ["pagey"]
