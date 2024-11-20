from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from binance_helper import Bot  # Assume your Bot class is saved in bot_class.py

app = Flask(__name__)
CORS(app)

# Path to the config file
CONFIG_FILE = "config.json"

@app.route('/update-config', methods=['POST'])
def update_config():
    """API to update Binance API keys in config.json"""
    try:
        data = request.json
        api_key = data.get('apiKey')
        api_secret = data.get('apiSecret')
        testnet = data.get('testnet', False)

        if not api_key or not api_secret:
            return jsonify({"status": "error", "message": "API key and secret are required"}), 400

        # Load existing config
        with open(CONFIG_FILE, 'r') as file:
            config = json.load(file)

        # Update the config with new keys
        config['EXCHANGES']['BINANCE-FUTURES']['API_KEY'] = api_key
        config['EXCHANGES']['BINANCE-FUTURES']['API_SECRET'] = api_secret
        config['EXCHANGES']['BINANCE-FUTURES']['TESTNET'] = testnet

        # Save updated config
        with open(CONFIG_FILE, 'w') as file:
            json.dump(config, file, indent=4)

        return jsonify({"status": "success", "message": "Config updated successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/execute-trade', methods=['POST'])
def execute_trade():
    """API to receive trade parameters and execute the bot's run function"""
    try:
        data = request.json

        # Extract and validate required parameters
        required_params = ["symbol", "type", "side", "qty", "leverage", "order_mode", "take_profit_percent", "stop_loss_percent"]
        missing_params = [param for param in required_params if param not in data]

        if missing_params:
            return jsonify({"status": "error", "message": f"Missing parameters: {', '.join(missing_params)}"}), 400

        # Load API keys from config
        with open(CONFIG_FILE, 'r') as file:
            config = json.load(file)

        api_key = config['EXCHANGES']['BINANCE-FUTURES']['API_KEY']
        api_secret = config['EXCHANGES']['BINANCE-FUTURES']['API_SECRET']
        testnet = config['EXCHANGES']['BINANCE-FUTURES']['TESTNET']

        # Initialize the bot
        bot = Bot(api_key, api_secret, testnet)

        # Execute the trade
        result = bot.run(data)

        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
