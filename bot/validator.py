def validate_side(side):
    if side.lower() not in ["buy", "sell"]:
        raise ValueError("Side must be BUY or SELL")
    
def validate_order_type(order_type):
    if order_type.lower() not in ["market", "limit"]:
        raise ValueError("Order type must be MARKET or LIMIT")
    
def validate_quantity(qty):
    if float(qty) <= 0:
        raise ValueError("Quantity must be positive")

def validate_price(price, order_type):
    if order_type.lower() == "limit" and price is None:
        raise ValueError("Price is required for LIMIT orders")  