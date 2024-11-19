import json
import ccxt
import random
import string
from custom_logging import logging

class Bot:
    def __init__(self, api_key, api_secret, testnet=False):
        try:
            self.exchange = ccxt.binance({
                'apiKey': api_key,
                'secret': api_secret,
                'options': {'defaultType': 'future'},
            })

            if testnet:
                self.exchange.set_sandbox_mode(True)

            self.clientId = None  # Unique client order ID generator
        except Exception as e:
            logging.error(f"Error initializing Bot: {str(e)}")
            raise ValueError(f"Failed to initialize Bot: {str(e)}")

    def create_string(self):
        """Generate a unique client order ID."""
        try:
            N = 7
            res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
            baseId = 'x-40PTWbMI'
            self.clientId = baseId + str(res)
            return self.clientId
        except Exception as e:
            logging.error(f"Error generating client order ID: {str(e)}")
            return None

    def fetch_order_status(self, order_id, symbol):
        """Fetch the status of a specific order."""
        try:
            order = self.exchange.fetch_order(order_id, symbol)
            return {'status': 'success', 'order_status': order['status']}
        except Exception as e:
            logging.error(f"Error fetching order status for {order_id}: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def place_stop_market(self, symbol, qty, stop_price, position_side):
        """Place a STOP_MARKET order for Stop Loss."""
        try:
            client_id = self.create_string()
            if not client_id:
                raise ValueError("Failed to generate client order ID.")

            order = self.exchange.create_order(
                symbol=symbol,
                side='SELL' if position_side == 'LONG' else 'BUY',
                type='STOP_MARKET',
                amount=qty,
                params={
                    "newClientOrderId": client_id,
                    'stopPrice': stop_price,
                    'closePosition': True,
                    'timeInForce': 'GTC'
                }
            )
            logging.info(f"STOP_MARKET order placed for {symbol}: SL={stop_price}")
            return {'status': 'success', 'order_id': order['id']}
        except Exception as e:
            logging.error(f"Error placing STOP_MARKET order: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def place_take_profit_market(self, symbol, qty, take_profit_price, position_side):
        """Place a TAKE_PROFIT_MARKET order for Take Profit."""
        try:
            client_id = self.create_string()
            if not client_id:
                raise ValueError("Failed to generate client order ID.")

            order = self.exchange.create_order(
                symbol=symbol,
                side='SELL' if position_side == 'LONG' else 'BUY',
                type='TAKE_PROFIT_MARKET',
                amount=qty,
                params={
                    "newClientOrderId": client_id,
                    'stopPrice': take_profit_price,
                    'closePosition': True,
                    'timeInForce': 'GTC'
                }
            )
            logging.info(f"TAKE_PROFIT_MARKET order placed for {symbol}: TP={take_profit_price}")
            return {'status': 'success', 'order_id': order['id']}
        except Exception as e:
            logging.error(f"Error placing TAKE_PROFIT_MARKET order: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def run(self, data):
        """Main method to execute a trade."""
        try:
            logging.info(f"Setting leverage {data['leverage']}%")
            self.exchange.load_markets()

            symbol = data['symbol']
            leverage = data['leverage']
            self.exchange.fapiprivate_post_leverage({
                'symbol': self.exchange.market(symbol)['id'],
                'leverage': leverage,
            })

            position_side = 'LONG' if data['side'] == 'Buy' else 'SHORT'

            if data['order_mode'] == 'Both':
                take_profit_percent = float(data['take_profit_percent']) / 100
                stop_loss_percent = float(data['stop_loss_percent']) / 100
                current_price = self.exchange.fetch_ticker(symbol)['last']

                if data['side'] == 'Buy':
                    take_profit_price = round(current_price * (1 + take_profit_percent), 2)
                    stop_loss_price = round(current_price * (1 - stop_loss_percent), 2)
                else:
                    take_profit_price = round(current_price * (1 - take_profit_percent), 2)
                    stop_loss_price = round(current_price * (1 + stop_loss_percent), 2)

                stop_market_result = self.place_stop_market(symbol, data['qty'], stop_loss_price, position_side)
                take_profit_market_result = self.place_take_profit_market(symbol, data['qty'], take_profit_price, position_side)

                if stop_market_result['status'] == 'error':
                    return {'status': 'error', 'message': f"Stop Market Error: {stop_market_result['message']}"}
                if take_profit_market_result['status'] == 'error':
                    return {'status': 'error', 'message': f"Take Profit Error: {take_profit_market_result['message']}"}

                return {
                    'status': 'success',
                    'stop_market_order': stop_market_result,
                    'take_profit_order': take_profit_market_result
                }

            return {'status': 'success', 'message': 'Trade executed successfully'}

        except Exception as e:
            logging.error(f"Error in run method: {str(e)}")
            return {'status': 'error', 'message': str(e)}
