Here's a `README.md` file for your project:

---

# Binance Trading Bot API

This project provides a Flask-based API for managing a Binance Futures trading bot. The bot allows you to:
1. Update Binance API keys in a configuration file (`config.json`).
2. Execute trades using the Binance Futures API.

---

## Features

- **Update Binance API Keys**: Update `config.json` with new API keys and testnet settings via an API.
- **Execute Trades**: Receive trade parameters and execute Stop Loss and Take Profit orders using the bot.
- **Error Handling**: Proper error responses with detailed messages for debugging.

---

## Prerequisites

### 1. **Python Dependencies**
Install the required Python packages:

```bash
pip install flask ccxt
```

### 2. **Configuration File**
Create a `config.json` file in the root directory with the following structure:

```json
{
    "EXCHANGES": {
        "BINANCE-FUTURES": {
            "API_KEY": "",
            "API_SECRET": "",
            "TESTNET": true
        }
    }
}
```

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/binance-trading-bot.git
   cd binance-trading-bot
   ```

2. Install dependencies:
   ```bash
   pip install flask ccxt
   ```

3. Run the Flask application:
   ```bash
   python app.py
   ```

---

## API Endpoints

### **1. Update API Keys**
- **Endpoint**: `/update-config`
- **Method**: `POST`
- **Description**: Updates Binance API keys and testnet settings in `config.json`.

#### Request:
```json
{
    "apiKey": "your_binance_api_key",
    "apiSecret": "your_binance_api_secret",
    "testnet": true
}
```

#### Response:
- Success:
  ```json
  {
      "status": "success",
      "message": "Config updated successfully"
  }
  ```
- Error:
  ```json
  {
      "status": "error",
      "message": "Error message here"
  }
  ```

---

### **2. Execute Trade**
- **Endpoint**: `/execute-trade`
- **Method**: `POST`
- **Description**: Executes a trade with Stop Loss and Take Profit orders.

#### Request:
```json
{
    "symbol": "BTC/USDT",
    "type": "market",
    "side": "Buy",
    "qty": 0.01,
    "leverage": 10,
    "order_mode": "Both",
    "take_profit_percent": 2.0,
    "stop_loss_percent": 1.0
}
```

#### Response:
- Success:
  ```json
  {
      "status": "success",
      "message": "Trade executed successfully",
      "stop_market_order": {"status": "success", "order_id": "12345"},
      "take_profit_order": {"status": "success", "order_id": "67890"}
  }
  ```
- Error:
  ```json
  {
      "status": "error",
      "message": "Error message here"
  }
  ```

---

## Example Usage

### Update Config:
```bash
curl -X POST http://127.0.0.1:5000/update-config \
-H "Content-Type: application/json" \
-d '{
    "apiKey": "your_binance_api_key",
    "apiSecret": "your_binance_api_secret",
    "testnet": true
}'
```

### Execute Trade:
```bash
curl -X POST http://127.0.0.1:5000/execute-trade \
-H "Content-Type: application/json" \
-d '{
    "symbol": "BTC/USDT",
    "type": "market",
    "side": "Buy",
    "qty": 0.01,
    "leverage": 10,
    "order_mode": "Both",
    "take_profit_percent": 2.0,
    "stop_loss_percent": 1.0
}'
```

---

## Project Structure

```
binance-trading-bot/
├── app.py           # Flask application
├── bot_class.py     # Trading bot logic
├── config.json      # Configuration file for Binance API keys
└── README.md        # Project documentation
```

---

## Notes

- **Testnet Mode**:
  - Set `"TESTNET": true` in `config.json` to use Binance Testnet for testing trades.
  - Testnet requires a separate account at [Binance Testnet](https://testnet.binancefuture.com/).

- **Production Mode**:
  - Set `"TESTNET": false` to execute trades on Binance's live environment.

- **Error Handling**:
  - Ensure all required parameters are provided in the API requests to avoid errors.

---

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

## Contributing

Feel free to open issues or submit pull requests to improve the bot.

---

This `README.md` file provides a comprehensive overview of your project and guides users on how to use the APIs effectively.