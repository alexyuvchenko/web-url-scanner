# Web URL Scanner

A Python-based web scanner that scans websites and generates reports of all links and broken links. Built with asyncio for efficient concurrent scanning.

## Features

- Asynchronous URL scanning
- Configurable scan depth
- Broken link detection
- CSV report generation
- Comprehensive logging
- Docker support
- Local development environment

## Prerequisites

- Python 3.13.1 or higher
- Docker and Docker Compose (for containerized usage)
- Make (optional, for using provided commands)

## Installation

### Using Docker (Recommended)

1. Build the Docker image:
```bash
make build
```

2. Run the scanner:
```bash
make up
```

3. View logs:
```bash
make logs
```

4. Stop the scanner:
```bash
make down
```

### Local Development

1. Set up local environment:
```bash
make setup-local
```

2. Run the scanner locally:
```bash
make run-local
```

3. Clean up local environment:
```bash
make clean-local
```

## Project Structure

```
web-url-scanner/
├── src/
│   └── web_url_scanner/
│       ├── __init__.py
│       ├── logger.py
│       └── scanner.py
├── scripts/
│   └── setup_local.sh
├── logs/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── pyproject.toml
└── README.md
```

## Available Commands

Run `make` or `make help` to see all available commands:

### Docker Commands
- `build` - Build Docker images
- `up` - Start containers
- `down` - Stop containers
- `logs` - View container logs

### Local Development Commands
- `setup-local` - Set up local development environment with .venv
- `run-local` - Run scanner in local environment
- `clean-local` - Remove virtual environment and cache files

## Configuration

The scanner can be configured through the following parameters:
- `base_url`: The starting URL for scanning
- `max_depth`: Maximum depth for recursive scanning (default: 3)

## Logs

Logs are stored in two locations:
- Console output (when running the scanner)
- `logs/scanner.log` file

## License

This project is licensed under the MIT License - see the LICENSE file for details.
