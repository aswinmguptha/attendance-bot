# Attendance Bot

A bot to mark user's attendance.

## Setup
Install dependencies (see [requirements.txt](./requirements.txt)), configure
environment variables (see below) and run with `python3 -m attendance_bot`.


### Environment variables
* `TG_BOT_TOKEN` - get a Telegram Bot Token from [@BotFather](https://telegram.dog/BotFather).

- The below [three] Environment Variables are optional.
* `USE_WEBHOOKS` - set this variable to `ANYTHING` to use WEBHOOKs mode, else the RoBot will use Long Polling.
* `PORT` (defaults to `5000`) - The port to listen at.
* `WEBHOOK_URL` (defaults to `http://localhost:5000/`) - The host to listen at.

