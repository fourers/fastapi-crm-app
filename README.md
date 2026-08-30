# Fast API CRM App

### Required Tools

- `docker compose`
- `just`
- `uv`
- `bun`
- `jq`

## Development

To install the required dependencies, run the following command:

```bash
just install
```

To initialise services (and wipe existing data), run the following command:

```bash
just init
```

To start the local development server, run the following command:

```bash
just dev
```

To build the frontend, run the following command:

```bash
just build
```

### Testing

> You should make a copy of `.env.sample` at `.env` i.e. `cp .env.sample .env`

To test creating a client, run the following command:

```bash
just examples/cli random-client
```

### Setting up SSL

It is assumed you have a private CA on your local machine (e.g. `mkcert`).

You will need to generate your own cert files and copy them to a path inside the project directory.

Once the certificates are available, add the following env variables to your `.env` file.

```bash
export KC_HOSTNAME="https://localhost/keycloak"
export CADDY_TLS_CONFIG="tls /app/certs/cert.pem /app/certs/key.pem"
export CADDY_SSL_KEY_FILE="./<PATH_TO_KEY_FILE>"
export CADDY_SSL_CERT_FILE="./<PATH_TO_CERT_FILE>"
```
