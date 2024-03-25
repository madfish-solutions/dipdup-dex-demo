# dipdup_indexer_dex_test_2

A blockchain indexer built with DipDup

## Installation

This project is based on [DipDup](https://dipdup.io), a framework for building featureful dapps.

You need a Linux/macOS system with Python 3.11 installed. To install DipDup with pipx for the current user:

```shell
curl -Lsf https://dipdup.io/install.py | python3
```

See the [Installation](https://dipdup.io/docs/installation) page for all options.

## Usage

Run the indexer in memory:

```shell
dipdup run
```

Store data in SQLite database:

```shell
dipdup -c . -c configs/dipdup.sqlite.yaml run
```

Or spawn a Compose stack with PostgreSQL and Hasura:

```shell
cd deploy
cp .env.default .env
# Edit .env file before running
docker-compose up
```

## Development setup

To set up the development environment:

```shell
poetry install
poetry shell
```

Run `make all` to run full CI check or `make help` to see other available commands.