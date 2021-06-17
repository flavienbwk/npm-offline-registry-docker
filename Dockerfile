FROM verdaccio/verdaccio:5.1.1

USER 0
RUN apk add --no-cache tzdata
ENV TZ "Europe/Paris"
USER $VERDACCIO_USER_UID

CMD node -r ./.pnp.js $VERDACCIO_APPDIR/bin/verdaccio --config /verdaccio/conf/config.yaml --listen $VERDACCIO_PROTOCOL://0.0.0.0:$VERDACCIO_PORT
