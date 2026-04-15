from pathlib import Path

import streamlit as st

from bot.logging_config import setup_logging
from bot.service import submit_order

LOG_FILE = Path("logs/app.logs")


def read_recent_logs(limit=25):
    if not LOG_FILE.exists():
        return "No logs yet."

    lines = LOG_FILE.read_text(encoding="utf-8", errors="ignore").splitlines()
    return "\n".join(lines[-limit:]) if lines else "No logs yet."


def main():
    setup_logging()

    st.set_page_config(page_title="Trading Bot", page_icon="TB", layout="centered")
    st.title("Trading Bot")
    st.caption("Lightweight Binance testnet order entry")

    if "order_type" not in st.session_state:
        st.session_state.order_type = "MARKET"

    with st.sidebar:
        st.subheader("Status")
        st.text(f"Log file: {LOG_FILE}")
        if LOG_FILE.exists():
            st.success("Logging ready")
        else:
            st.info("Log file will be created on first action")

    symbol = st.text_input("Symbol", value="BTCUSDT")
    side = st.selectbox("Side", ["BUY", "SELL"])
    order_type = st.selectbox("Order Type", ["MARKET", "LIMIT"], key="order_type")

    with st.form("order_form"):
        quantity = st.text_input("Quantity", value="0.001")
        price = st.text_input(
            "Price",
            value="",
            disabled=order_type != "LIMIT",
            help="Required only for limit orders.",
        )
        submitted = st.form_submit_button("Place Order", use_container_width=True)

    if submitted:
        try:
            payload, order = submit_order(symbol, side, order_type, quantity, price)
            st.success("Order request submitted.")
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Order Input")
                st.json(payload)
            with col2:
                st.subheader("Exchange Response")
                st.json(order)
        except Exception as exc:
            st.error(str(exc))

    st.subheader("Recent Logs")
    st.code(read_recent_logs(), language="text")


if __name__ == "__main__":
    main()
