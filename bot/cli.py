import argparse

from bot.logging_config import setup_logging
from bot.service import submit_order


def run():
    setup_logging()

    parser = argparse.ArgumentParser(description="Trading Bot CLI")

    parser.add_argument("--symbol", required=True)
    parser.add_argument("--side", required=True)
    parser.add_argument("--type", required=True)
    parser.add_argument("--quantity", required=True)
    parser.add_argument("--price", required=False)

    args = parser.parse_args()

    try:
        payload, order = submit_order(
            args.symbol,
            args.side,
            args.type,
            args.quantity,
            args.price,
        )

        print("\nOrder Summary:")
        print(payload)

        if order.get("status") == "FILLED":
            print("Order Filled Successfully!")
        else:
            print("\nOrder placed but not filled yet.")

        print(f"Order ID: {order.get('orderId')}")
        print(f"Status: {order.get('status')}")
        print(f"Executed Qty: {order.get('executedQty')}")
        print(f"Avg Price: {order.get('avgPrice', 'N/A')}")

    except Exception as e:
        print("\nError:", str(e))
