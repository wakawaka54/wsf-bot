# wsf-bot

![Static Badge](https://img.shields.io/badge/version-v0.4-green?style=for-the-badge)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/wakawaka54/wsf-bot/deploy.yml?style=for-the-badge)
![GitHub top language](https://img.shields.io/github/languages/top/wakawaka54/wsf-bot?style=for-the-badge)
![GitHub](https://img.shields.io/github/license/wakawaka54/wsf-bot?style=for-the-badge)
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/wakawaka54/wsf-bot/main?style=for-the-badge)

This bot will periodically check the Washington State Ferry reservation
website for availability on a set of configured routes. If available routes are
found, the bot will send a notification via Discord. 

**This bot will not make reservations for you.** You will still
need to make the reservation after receiving the notification.

Use this bot at **your own risk**. Be responsible and do not
abuse this functionality.

# Getting started

## Run hosted

Honestly, I run this on my personal unraid server. The app
is fully containerized so you can run it in the cloud provider of
your choice.

Most cloud providers support running a Docker container application,
see the **Config** section below for setup help.

## Run with docker

* Clone the repo
* Copy `example.config.yml` to `config.yml` and edit it
* `docker-compose up`

# Config

## Config file

This is the recommended method but may be hard to
do some cloud provider platforms.

* Clone the repo
* Copy `example.config.yml` to `config.yml` and edit to your preference.
* Run the container with the `config.yml` mounted:
    ```shell
   docker run -v config.yml:/usr/bot/config.yml ghcr.io/wakawaka54/wsf-bot:latest
    ```
  or through docker-compose
  ```shell
  docker-compose up
  ```

## Environment variable

Alternatively, the bot can be configured through a simple environment variable, 
`WSF_BOT_CONFIG` which is set to the **JSON** representation of the `config.yml`.

* Clone the repo
* Copy `example.config.yml` to `config.yml` and edit to your preference.
* Use an online YAML-to-JSON converter such as [this](https://jsonformatter.org/yaml-to-json).
* Run the container with the `WSF_BOT_CONFIG` variable set:
    ```shell
    export WSF_BOT_CONFIG='<JSON Config>'
    docker run -e WSF_BOT_CONFIG="${WSF_BOT_CONFIG}" ghcr.io/wakawaka54/wsf-bot:latest
    ```

