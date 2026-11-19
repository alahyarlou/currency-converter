import requests
from cachetools import TTLCache, cached

# Cache exchange rates for 300 seconds, with a maximum of 100 entries.
cache: TTLCache = TTLCache(maxsize=100, ttl=300)


@cached(cache)
def get_exchange_rate(
    base_currency: str,
    target_currency: str,
) -> tuple[float, int] | None:
    """Retrieve the exchange rate between two currencies.

    Fetches the latest exchange rates from ExchangeRate-API.
    Results are cached for 3 hours to reduce unnecessary API requests.

    Args:
        base_currency: The currency code to convert from (e.g., 'USD').
        target_currency: The currency code to convert to (e.g., 'EUR').

    Returns:
        A tuple containing the exchange rate and the last update
        timestamp, or None if the request fails or the currency
        is not available.
    """
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return None

        data = response.json()
        exchange_rate: float = data["rates"][target_currency]
        last_updated: int = data["time_last_updated"]

        return exchange_rate, last_updated

    except (requests.RequestException, KeyError, ValueError):
        return None


def convert_currency(amount: float, exchange_rate: float) -> float:
    """Convert an amount from one currency to another.

    Args:
        amount: The amount of money in the base currency.
        exchange_rate: The exchange rate between the two currencies.

    Returns:
        float: The converted amount in the target currency.
    """
    return amount * exchange_rate


if __name__ == "__main__":
    base_currency: str = input("Enter base currency: ").upper()
    target_currency: str = input("Enter target currency: ").upper()
    amount: float = float(input("Enter amount: "))

    result = get_exchange_rate(base_currency, target_currency)

    if result is not None:
        exchange_rate, last_updated = result

        converted_amount: float = convert_currency(amount, exchange_rate)

        print(
            f"{amount} {base_currency} is " f"{converted_amount:.2f} {target_currency}"
        )

        print(f"Last updated timestamp: {last_updated}")

    else:
        print("Unable to retrieve the exchange rate.")
