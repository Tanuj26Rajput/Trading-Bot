from bot.client import get_client
import logging
import time

def place_order(symbol, side, order_type, quantity, price=None):
    client = get_client()

    try:
        logging.info(f"Placing {order_type} order: {symbol} {side}")

        if order_type.lower() == "market":
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=quantity
            )

        elif order_type.lower() == "limit":
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                quantity=quantity,
                price=price,
                timeInForce="GTC"
            )

        time.sleep(2)
        updated_order = check_order_status(client, symbol, order["orderId"])

        logging.info(f"Updated Order Status: {updated_order}")
        return updated_order
    
    except Exception as e:
        logging.error(f"order failed: {str(e)}")
        raise Exception(f"Order failed: {str(e)}")
    
def check_order_status(client, symbol, order_id):
    try:
        order = client.futures_get_order(
            symbol=symbol,
            orderId=order_id
        )
        return order
    except Exception as e:
        return {"error": str(e)}
    
