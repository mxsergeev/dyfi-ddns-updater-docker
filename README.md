# dyfi-ddns-updater-docker

A simple Dockerized Python script to update multiple dy.fi dynamic DNS hostnames automatically. It periodically checks your public IP and updates dy.fi if your IP changes or after a set interval.

## Features

- Supports multiple dy.fi hostnames
- Stores state and logs in a persistent volume
- Configurable via environment variables
- Runs as a Docker container

## Usage

### 1. Clone the repository

```
git clone <this-repo-url>
cd dyfi-ddns-updater-docker
```

### 2. Configure Environment Variables

Create a `.env` file or set the following variables:

- `DYFI_USER` – your dy.fi username
- `DYFI_PASS` – your dy.fi password
- `DYFI_HOSTS` – comma-separated list of dy.fi hostnames (e.g. `myhost1.dy.fi,myhost2.dy.fi`)
- `DYFI_STATE_DIR` – (optional) directory for state files (default: `/data`)
- `DYFI_LOG_FILE` – (optional) log file path (default: logs to stdout)

### 3. Run with Docker Compose

```
docker-compose up -d --build
```

### 4. Data Persistence

State and logs are stored in the `./data` directory, mapped to `/data` in the container.

## File Structure

- `dyfi_ddns_updater.py` – main updater script
- `requirements.txt` – Python dependencies
- `Dockerfile` – container build instructions
- `docker-compose.yaml` – service configuration
- `data/` – persistent state and logs

## License

MIT
