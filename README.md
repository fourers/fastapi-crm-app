# Fast API CRM App

### Required Tools

- `docker`
- `just`
- `uv`
- `bun`

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
just cli random-client
```
