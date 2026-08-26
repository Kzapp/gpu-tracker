# GPU Tracker

GPU Tracker is a web scraper built specifically for Newegg's website. It allows a user to input a maximum price, then scans Newegg for in-stock GPUs matching that budget and sends alerts with product links directly to an email inbox.

## Features

- Built with a proper **OOP structure** — a `GpuStock` class handling scraping, filtering, and email alerts
- **Multi-layered error handling** — separate handling for network-level failures (timeouts, connection errors) and data-level failures (malformed pricing data), so one bad listing never crashes the whole scan
- **Safe credential storage** — Gmail sender, receiver, and app password are loaded from a `.env` file, never hardcoded in the source code
- **Interactive menu** — run a one-time check, schedule automatic hourly checks, or exit cleanly

## Requirements

- Python 3 (developed with 3.14)
- Install dependencies:

```bash
pip install -r requirements.txt
```

- A `.env` file in the project root containing:

```
GMAIL_SENDER=your-email@gmail.com
GMAIL_RECEIVER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-gmail-app-password
```

(Use a [Gmail App Password](https://myaccount.google.com/apppasswords), not your real account password.)

## How to Run

The program runs through `main.py`, which imports the `GpuStock` class from `gpu_script.py`.

```bash
python3 main.py
```

You'll be asked for a maximum price, then given a menu:
1. Check Newegg once, immediately
2. Check Newegg automatically every hour
3. Exit

## Project History

This project was originally built as an early, copy-pasted script with no real understanding behind it — no error handling, no structure, and a hardcoded password. It was later fully rewritten from scratch with a genuine understanding of OOP, proper exception handling, and secure credential management, as a direct before-and-after demonstration of that growth.
