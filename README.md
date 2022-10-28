[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg?logo=python)](https://www.python.org)
[![codecov](https://codecov.io/gh/leandcesar/bobotinho-bot/branch/master/graph/badge.svg)](https://codecov.io/gh/leandcesar/bobotinho-bot)
[![License](https://img.shields.io/badge/license-AGPL%20v3-yellow.svg)](https://github.com/leandcesar/bobotinho-bot/blob/main/LICENSE)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
<!-- [![build](https://github.com/leandcesar/bobotinho-bot/workflows/CI/badge.svg)](https://github.com/leandcesar/bobotinho-bot/actions/workflows/ci.yml) -->
<!-- [![UptimeRobot](https://img.shields.io/uptimerobot/status/m788541737-d1097381d469c36beb1e16b3)](https://stats.uptimerobot.com/EQQpJSWDE5/788541737) -->

# Bobotinho

## ‎💻 Technologies
- [**twitchio 2**](https://twitchio.dev/en/latest/) is a fully asynchronous Python IRC, API, EventSub and PubSub library for Twitch
- [**pynamodb**](https://pynamodb.readthedocs.io/en/latest/) is a Pythonic interface to Amazon’s DynamoDB
- [**aiohttp**](https://docs.aiohttp.org/en/stable/) us an asynchronous HTTP Client/Server for asyncio and Python

## 🧰 Services
- [**Bugsnag**](https://www.bugsnag.com/) is an error monitoring and reporting software
- [**The Color API**](https://www.thecolorapi.com/) is a swiss army knife for color available as a API
- [**CoinAPI**](https://www.coinapi.io/) is a platform which provides data APIs to cryptocurrency markets
- [**Dashbot**](https://www.dashbot.io/) is a data platform that ingests, cleans, stores, and processes any type of Conversation Data
- [**math.js**](https://api.mathjs.org/) is an extensive math library available as a API
- [**OpenWeather**](https://openweathermap.org/) provides global weather data available as a API
- [**Wit.ai**](https://wit.ai/) is an open source framework with advanced natural language processing available as a API

## 🏁 Getting Started
It is assumed that you have:
- [**Twitch**](https://twitch.tv/) account for your bot
- [**Python +3.9**](https://www.python.org/) installed
- [**Pip**](https://pip.pypa.io/en/stable/) installed

```bash
$ python3 --version
$ pip3 --version
```

## 🔒 Access Token

Visit [**Token Generator**](https://twitchtokengenerator.com/) and select the "Bot Chat Token". After selecting this you can copy your "Access Token" somewhere safe.

## ⚙️ Configuring

After clone this repo, create `.env` file in your `/bobotinho` directory. Add the access token from above and dev nick after the `=`. Optionally add and fill other env vars (see `.env.template`).

```
BOT_TOKEN=your-token-here
BOT_SECRET=your-secrete-here
DEV_NICK=your-twitch-nick
```

## ▶️ Run 

### 🏠 Option 1: with `make`

```bash
$ make install
$ make run
```

### 🐋 Option 2: with `docker`

It is assumed that you have [**Docker**](https://www.docker.com/) installed.

```bash
$ docker --version
```

Otherwise, you can download and install Docker [**here**](https://docs.docker.com/get-docker/).

```bash
$ docker build -t bobotinho .
$ docker run --env-file=.env bobotinho
```

### 🐳 Option 3: with `docker-compose`

It is assumed that you have [**Docker**](https://www.docker.com/) and **Docker Compose** installed.

```bash
$ docker --version
$ docker-compose --version
```

Otherwise, you can download and install Docker Compose [**here**](https://docs.docker.com/compose/install/).

```bash
$ docker-compose up
```

### 🎉 Use

Go to [twitch.tv/`DEV_NICK`](https://twitch.tv/) and send `%ping`.
