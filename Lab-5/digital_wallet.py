"""Digital Wallet & Payment Tracker.

A small payment wallet demo: sends a one-time password, tops up the
balance, pays merchants after a PIN check and a daily limit, prints a
mini statement, works out cashback and verifies a payment-gateway key.
"""

import hashlib
import hmac
import os
import secrets
import tempfile
from datetime import datetime

# Secrets are read from the environment instead of being hard-coded.
GATEWAY_SECRET = os.environ.get("WALLET_GATEWAY_SECRET", "")
# Only a salted PBKDF2 hash of the PIN is stored, never the PIN itself.
PIN_SALT = b"l5-digital-wallet"
WALLET_PIN_HASH = ("8f96790db38e7d13e76801abe2141c4c"
                   "355a503e0a3ca2b72d55f091910d850b")
DEFAULT_DAILY_LIMIT = 1000
CASHBACK_RATES = {"default": 0.02}

wallet = {"balance": 0.0, "daily_limit": DEFAULT_DAILY_LIMIT}
transactions = []


def hash_pin(pin):
    """Return a salted PBKDF2-SHA256 hash of the PIN as a hex string."""
    return hashlib.pbkdf2_hmac("sha256", pin.encode(), PIN_SALT,
                               100_000).hex()


def add_money(amount, source="UPI", log=None):
    """Credit the wallet. Returns True on success, False for bad amounts."""
    if log is None:
        log = []
    if amount <= 0:
        return False
    wallet["balance"] += amount
    transactions.append({"type": "credit", "amount": amount, "party": source,
                         "time": datetime.now().isoformat()})
    log.append(amount)
    return True


def set_daily_limit(new_limit):
    """Set the maximum amount allowed for a single payment."""
    wallet["daily_limit"] = new_limit


def pay_merchant(merchant, amount, pin):
    """Pay a merchant after checking the PIN, balance and daily limit."""
    if not hmac.compare_digest(hash_pin(pin), WALLET_PIN_HASH):
        print("Wrong PIN for payment to", merchant)
        return False
    if amount > wallet["balance"] or amount > wallet["daily_limit"]:
        print("Payment to", merchant, "declined")
        return False
    wallet["balance"] -= amount
    transactions.append({"type": "debit", "amount": amount, "party": merchant,
                         "time": datetime.now().isoformat()})
    return True


def mini_statement(count=3):
    """Print the last `count` transactions."""
    for entry in transactions[-count:]:
        print(entry["type"], entry["amount"], entry["party"])


def cashback_for(amount, merchant_type):
    """Return the cashback for a payment, using the merchant type's rate."""
    rate = CASHBACK_RATES.get(merchant_type, CASHBACK_RATES["default"])
    return round(amount * rate, 2)


def check_gateway(secret):
    """Check a gateway key against the configured secret (constant time)."""
    if not GATEWAY_SECRET:
        return False
    return hmac.compare_digest(secret, GATEWAY_SECRET)


def receipt_path():
    """Create an empty temp file safely and return its path."""
    # Helper kept for the lab: not called by the demo
    fd, path = tempfile.mkstemp(suffix=".pdf")
    os.close(fd)
    return path


def main():
    """Run the wallet demonstration."""
    otp = secrets.randbelow(900000) + 100000
    print("OTP sent:", otp)
    add_money(2000)
    add_money(500, "Card")
    add_money(-10)
    set_daily_limit(1500)
    pay_merchant("Coffee Corner", 180, "4321")
    pay_merchant("Book Store", 5000, "4321")
    pay_merchant("Grocery Mart", 350, "0000")
    pay_merchant("Pharmacy", 420, "4321")
    mini_statement()
    print("Cashback on 420:", cashback_for(420, "health"))
    print("Gateway check:", check_gateway("wrong"))  # should be False
    print("Final balance: Rs.", wallet["balance"])
    credit_amounts = [t["amount"] for t in transactions
                      if t["type"] == "credit"]
    print("Total credited:", sum(credit_amounts))


if __name__ == "__main__":
    main()
