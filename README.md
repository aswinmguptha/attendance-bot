# Attendance Bot

We've always wanted to make your lives easier. We get that the struggle of managing attendance is real, but we also know that the power of technology is unmatched. So we created our own Attendance Bot for Telegram to cut down on time and effort you spend on attendance. We hope you will enjoy Group Attendance Bot as much as we did building it. Check out [CONTRIBUTING.md](CONTRIBUTING.md) to contribute to the project. If you are interested in translating the bot to any languages, check out [locale/README.md](locale/README.md). Thank you for your support.

## Setup
Install dependencies (see [requirements.txt](./requirements.txt)), configure
environment variables (see below) and run with `python3 -m attendance_bot`.


### Environment variables
* `TG_BOT_TOKEN` - get a Telegram Bot Token from [@BotFather](https://telegram.dog/BotFather).

- The below [three] Environment Variables are optional.
* `USE_WEBHOOKS` - set this variable to `ANYTHING` to use WEBHOOKs mode, else the RoBot will use Long Polling.
* `PORT` (defaults to `5000`) - The port to listen at.
* `WEBHOOK_URL` (defaults to `http://localhost:5000/`) - The host to listen at.
