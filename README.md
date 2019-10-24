# yarn-offline-mirror-docker

Dockerized Yarn / NPM / PNPM offline mirror / registry to host your dependencies.

## Getting started

### Setting up credentials for registry (offline)

In order for you to be able to **push** packages on the registry, you need to create a user account.  
The default credentials are : username `default` and password `default`.

Credentials are stored in `registry/conf/htpasswd`

To add a user :

```
apt install apache2-utils -y
htpasswd ./registry/conf/htpasswd myuser
docker-compose restart mirror
```

To remove a user, just remove its line in `registry/conf/htpasswd` and restart the `mirror` container

### Downloading your dependencies (online)

### Pushing your dependencies to your local registry (offline)

### Testing if everything works (offline)

### Installing your offline client (offline)