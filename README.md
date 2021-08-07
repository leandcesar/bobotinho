![https://www.python.org](https://img.shields.io/badge/Python-3.8+-blue.svg) ![https://github.com/leandcesar/bobotinho/blob/master/LICENSE](https://img.shields.io/badge/license-AGPL%20v3-lightgray.svg) ![https://github.com/psf/black](https://img.shields.io/badge/code%20style-black-000000.svg) ![https://bobotinho.vercel.app](https://img.shields.io/badge/site-bobotinho-9147ff.svg) ![https://discord.gg/6Ue66Vs5eQ](https://img.shields.io/badge/discord-bobotinho-7289da.svg)

# Bobotinho
Main repository for the chatbot Bobotinho.

## ℹ️ Introduction
Twitch chatbot with entertainment commands.

### ‎💻 Technologies
- [**asyncio**](https://docs.python.org/3/library/asyncio.html)
- [**AIOHTTP**](https://docs.aiohttp.org/en/stable/)
- [**PostgreSQL**](https://www.postgresql.org/)
- [**Redis**](https://redis.io/)
- [**TwitchIO 2**](https://twitchio.readthedocs.io/en/latest/index.html)
- [**Tortoise ORM**](https://tortoise-orm.readthedocs.io/en/latest/)


## 🏁 Getting Started
It is assumed that you have:
- [**Twitch**](https://twitch.tv/) account for your bot.
- [**Python 3.8+**](https://www.python.org/) installed.
- [**Pip**](https://pip.pypa.io/en/stable/) installed.

```bash
$ python3 --version
$ pip3 --version
```

### 🔒 Access Token

Visit [**Token Generator**](https://twitchtokengenerator.com/) and select the "Bot Chat Token". After selecting this you can copy your "Access Token" somewhere safe.

### ⚙️ Configuring

After clone this repo, create `.env` file in your `/bobotinho-bot` directory. Add the access token from above and owner nick after the `=`. Optionally add and fill other env vars (see `.env.template`).

```
ACCESS_TOKEN=your-token-here
OWNER=your-twitch-nick
```

### Run 

#### 🏠 Option 1: locally

The standard library as of Python 3.3 comes with a concept called "Virtual Environment"s to keep libraries from polluting system installs or to help maintain a different version of libraries than the ones installed on the system.

Execute the following commands in your `/bobotinho-bot` directory:

```bash
$ python3.8 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ env/bin/python bot.py
```

#### 🐋 Option 2: with `docker`

It is assumed that you have [**Docker**](https://www.docker.com/) installed.

```bash
$ docker --version
```

Otherwise, you can download and install Docker [**here**](https://docs.docker.com/get-docker/).

Execute the following commands in your `/bobotinho-bot` directory:

```bash
$ docker build -t bobotinho-bot .
$ docker run bobotinho-bot
```

#### 🐳 Option 3: with `docker-compose`

It is assumed that you have [**Docker**](https://www.docker.com/) and **Docker Compose** installed.

```bash
$ docker --version
$ docker-compose --version
```

Otherwise, you can download and install Docker Compose [**here**](https://docs.docker.com/compose/install/).

Execute the following commands in your `/bobotinho-bot` directory:

```bash
$ docker-compose up --build
```

> *Use `--build` flag only the first run*

### 🎉 Use

Go to Twitch channel set on `OWNER` and send `%ping`.
