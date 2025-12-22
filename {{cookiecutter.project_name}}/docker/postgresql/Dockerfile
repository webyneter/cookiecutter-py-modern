# syntax=docker/dockerfile:1
# https://hub.docker.com/_/postgres
FROM postgres:17.7

COPY --chmod=755 scripts/ /usr/local/bin/
COPY --chmod=755 entrypoint.bash /usr/local/bin/entrypoint

ENTRYPOINT ["/usr/local/bin/entrypoint"]
CMD ["postgres"]
