# Trading Bot

A small Binance Futures testnet trading bot with two ways to place orders:

- a command-line interface for quick runs
- a lightweight Streamlit UI for manual order entry

This project is intentionally simple. The code is split into small modules so validation, exchange access, logging, and UI logic stay separate and easier to understand.

## What This Project Does

The bot:

- loads API credentials from `.env`
- validates order input
- creates a Binance Futures testnet client
- submits a `MARKET` or `LIMIT` order
- waits briefly and fetches the updated order status
- logs important activity to `logs/app.logs`

## Project Structure

```text
Trading Bot/
|-- bot/
|   |-- cli.py
|   |-- client.py
|   |-- logging_config.py
|   |-- orders.py
|   |-- service.py
|   |-- validator.py
|-- logs/
|   |-- app.logs
|-- .env
|-- .env-example
|-- main.py
|-- requirements.txt
|-- streamlit_app.py
```

## Setup

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root. You can copy the values from `.env-example`:

```env
API_KEY="your_binance_testnet_api_key"
API_SECRET="your_binance_testnet_secret_key"
```

These keys should be for Binance testnet, not your real trading account.

## How To Run

### Option 1: Run without Streamlit (CLI)

This uses the command-line entry point from `main.py`.

Example `MARKET` order:

```powershell
python main.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

Example `LIMIT` order:

```powershell
python main.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 70000
```

What happens:

- `main.py` starts the CLI
- the CLI parses arguments
- the shared service validates and normalizes input
- the order module sends the order to Binance
- the result is printed in the terminal

### Option 2: Run with Streamlit UI

```powershell
streamlit run streamlit_app.py
```

Then open the local URL shown by Streamlit, usually:

```text
http://localhost:8501
```

What you can do in the UI:

- enter symbol, side, order type, quantity, and price
- place `MARKET` or `LIMIT` orders
- see the submitted payload
- see the exchange response
- read the most recent log lines

## File-By-File Explanation

### `main.py`

Purpose:
Starts the CLI version of the bot.

How it works:

- imports `run` from `bot.cli`
- calls it when the file is executed directly

Why it exists:
Keeps the root entry point very small and delegates real logic to the `bot/` package.

### `streamlit_app.py`

Purpose:
Provides a lightweight browser-based UI for the bot.

How it works:

- sets up logging
- renders inputs for symbol, side, order type, quantity, and price
- calls the shared `submit_order()` function from `bot.service`
- shows both the cleaned request payload and Binance response
- reads `logs/app.logs` and displays recent log entries

Why it exists:
Lets you use the same trading flow without typing CLI commands.

### `bot/cli.py`

Purpose:
Implements the command-line interface.

How it works:

- defines the supported CLI arguments
- calls `setup_logging()`
- passes user input to `submit_order()`
- prints the order summary and order result

Why it exists:
Keeps CLI-specific behavior separate from business logic.

### `bot/service.py`

Purpose:
Acts as the shared application layer used by both the CLI and Streamlit UI.

How it works:

- normalizes raw input
  - symbol is uppercased and trimmed
  - side and type are uppercased and trimmed
  - quantity and price are converted to strings
- validates input using `bot.validator`
- builds a clean payload dictionary
- calls `place_order()` from `bot.orders`
- returns both the cleaned payload and exchange response

Why it exists:
This is the glue between interfaces and trading logic. Without it, CLI and UI would duplicate validation and submission code.

### `bot/validator.py`

Purpose:
Validates order input before anything is sent to Binance.

How it works:

- `validate_side()` allows only `BUY` or `SELL`
- `validate_order_type()` allows only `MARKET` or `LIMIT`
- `validate_quantity()` ensures quantity is positive
- `validate_price()` requires a price for limit orders

Why it exists:
Bad input is rejected early, before the bot makes an API call.

### `bot/client.py`

Purpose:
Creates the Binance API client.

How it works:

- loads environment variables using `python-dotenv`
- reads `API_KEY` and `API_SECRET`
- creates a `binance.client.Client` with `testnet=True`
- sets futures leverage for `BTCUSDT`
- returns the client object to the rest of the application

Why it exists:
All exchange connection setup is isolated in one place.

Important note:
This file currently hardcodes `BTCUSDT` when changing leverage. If you place orders for another symbol, you may want to update this behavior.

### `bot/orders.py`

Purpose:
Contains the exchange-facing order placement logic.

How it works:

- gets a configured Binance client from `bot.client`
- logs the order attempt
- chooses the correct Binance API call based on order type
  - `MARKET` uses `futures_create_order(..., type="MARKET")`
  - `LIMIT` uses `futures_create_order(..., type="LIMIT", timeInForce="GTC")`
- waits 2 seconds
- fetches the updated order status using `check_order_status()`
- returns the latest order information

Why it exists:
This module is responsible for actual order submission and follow-up status retrieval.

### `bot/logging_config.py`

Purpose:
Configures application logging.

How it works:

- creates the `logs/` folder if it does not exist
- writes logs to `logs/app.logs`
- uses the format:
  - timestamp
  - log level
  - message

Why it exists:
It gives both the CLI and UI a shared log destination and avoids scattering logging setup across files.

### `logs/app.logs`

Purpose:
Stores runtime logs.

What goes here:

- order placement attempts
- updated order status
- failures and exception details

Why it matters:
This is the easiest place to check what happened during a run.

### `.env-example`

Purpose:
Shows the expected environment variable names.

Why it exists:
It acts as a template so new users know what must be added to `.env`.

### `.env`

Purpose:
Stores your local Binance testnet credentials.

Why it exists:
Secrets should not be hardcoded inside Python files.

## Architecture Overview

The project has a simple layered architecture:

```text
CLI (main.py -> bot/cli.py)        Streamlit UI (streamlit_app.py)
                \                  /
                 \                /
                  -> bot/service.py
                         |
                  validation layer
                  (bot/validator.py)
                         |
                  order execution layer
                  (bot/orders.py)
                         |
                  exchange client layer
                  (bot/client.py)
                         |
                     Binance Testnet

Shared across all layers:
- bot/logging_config.py
- logs/app.logs
```

## Request Flow

When you place an order, the flow is:

1. You provide input through the CLI or Streamlit UI.
2. The interface sends the raw input to `bot.service.submit_order()`.
3. `submit_order()` cleans and validates the values.
4. If validation passes, `bot.orders.place_order()` is called.
5. `place_order()` gets a Binance client from `bot.client.get_client()`.
6. The order is sent to Binance Futures testnet.
7. The bot waits briefly and fetches the latest order status.
8. The result is returned to the CLI or UI.
9. Important steps are written to `logs/app.logs`.

## How The Pieces Work Together

The separation of responsibilities is the main architectural idea:

- interfaces collect input
- the service layer coordinates the use case
- validators protect the system from bad input
- the orders module handles exchange calls
- the client module handles API setup
- the logging module handles observability

This makes the bot easier to extend. For example:

- you can add another UI without changing Binance order code
- you can add more validation rules without changing the CLI
- you can replace the exchange client setup in one place

## Current Limitations

- only `MARKET` and `LIMIT` orders are supported
- logging is file-based only
- leverage setup is hardcoded for `BTCUSDT`
- there are no automated tests yet
- there is no retry, risk management, or position tracking layer yet

## Quick Troubleshooting

### `API_KEY` or `API_SECRET` errors

Check that:

- `.env` exists in the project root
- variable names exactly match `API_KEY` and `API_SECRET`
- you are using Binance testnet credentials

### `Price is required for LIMIT orders`

This means:

- the selected order type is `LIMIT`
- no price was provided

### Order rejected by Binance

Possible reasons:

- invalid symbol
- quantity too small
- price not valid for the symbol
- testnet account configuration issue

### No logs appearing

Check that:

- `setup_logging()` is being called
- the `logs/` folder exists
- the process has permission to write files

## Suggested Next Improvements

- make leverage configurable per symbol
- add symbol validation
- add better error handling around Binance API responses
- add tests for validators and service logic
- show friendlier order status messages in the UI
