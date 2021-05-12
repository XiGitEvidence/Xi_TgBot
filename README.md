# Xi_TgBot

Telegram Bot For xi-speech-synthesizer


## Usage

Only Inline mode.

https://telegram.org/blog/inline-bots


## Args

* **BOT_TOKEN**

  Each bot is given a unique authentication token when it is created.

* **XI_API**

  To `xi-speech-synthesizer` API URL.

* THIS_URL

  URL for Current service can access from Internet.

  Frontend reverse proxy requires SSL support.

  https://core.telegram.org/bots/webhooks

## Deploy

```bash
    docker build -t xi_tgbot .
    docker run -d -p 5000:5000 -e BOT_TOKEN="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11" -e XI_API="http://xi-speech-synthesizer" -e THIS_URL="https://example.com/tgbot"  xi_tgbot
```