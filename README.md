# dyfi-ddns-updater-docker

A simple Dockerized Python script to update multiple dy.fi dynamic DNS hostnames automatically. It periodically checks your public IP and updates dy.fi if your IP changes or after six days since the last update have passed (as per dy.fi's policy).

## Features

- Update as many dy.fi hostnames as needed
- Configurable via environment variables
- Runs as a Docker container

## Usage

### 1. Clone the repository

```bash
git clone https://github.com/mxsergeev/dyfi-ddns-updater-docker.git
cd dyfi-ddns-updater-docker
```

### 2. Configure Environment Variables

Create a `.env` file or set the following variables:

- `DYFI_USER` – your dy.fi username
- `DYFI_PASS` – your dy.fi password
- `DYFI_HOSTS` – comma-separated list of dy.fi hostnames (e.g. `myhost1.dy.fi,myhost2.dy.fi`)

See `.env.example` for a template.

### 3. Run with Docker Compose

```bash
docker compose up -d --build
```

### 4. Check Logs

Check logs to see if the updater is working correctly:

```bash
docker compose logs -f
```

### 5. Fresh start

If you want to start fresh, you can remove the Docker volume that stores the state:

```bash
docker compose down
docker volume rm dyfi-ddns-updater-docker_dyfi-data
```

## License

MIT
