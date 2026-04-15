from bot.orders import place_order
from bot.validator import (
    validate_order_type,
    validate_price,
    validate_quantity,
    validate_side,
)


def submit_order(symbol, side, order_type, quantity, price=None):
    normalized_symbol = symbol.upper().strip()
    normalized_side = side.upper().strip()
    normalized_type = order_type.upper().strip()
    normalized_quantity = str(quantity).strip()
    normalized_price = None if price in (None, "") else str(price).strip()

    validate_side(normalized_side)
    validate_order_type(normalized_type)
    validate_quantity(normalized_quantity)
    validate_price(normalized_price, normalized_type)

    payload = {
        "symbol": normalized_symbol,
        "side": normalized_side,
        "type": normalized_type,
        "quantity": normalized_quantity,
        "price": normalized_price,
    }

    order = place_order(
        normalized_symbol,
        normalized_side,
        normalized_type,
        normalized_quantity,
        normalized_price,
    )

    return payload, order
