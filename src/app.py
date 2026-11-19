from datetime import datetime

import currencies
import humanize
import streamlit as st

from currency_converter import convert_currency, get_exchange_rate


def main() -> None:
    """Run the Streamlit currency converter application.

    Allows users to select base and target currencies, enter an amount,
    retrieve the latest exchange rate, and display the converted amount
    along with the time since the rate was last updated.
    """
    st.title(":dollar: Currency Converter")

    st.markdown("""
        This tool allows you to instantly convert amounts between
        different currencies 🌍.

        Enter the amount and choose the currencies to see the result.
        """)

    # Get available currency codes.
    currency_codes: list[str] = list(currencies.MONEY_FORMATS.keys())

    # Currency selection.
    base_currency: str = st.selectbox(
        label="From Currency (Base):",
        options=currency_codes,
    )

    target_currency: str = st.selectbox(
        label="To Currency (Target):",
        options=currency_codes,
    )

    # Get the amount to convert.
    amount: float = st.number_input(
        label="Amount To Convert:",
        min_value=0.0,
        value=100.0,
    )

    # Perform currency conversion.
    if amount > 0 and base_currency and target_currency:
        result = get_exchange_rate(base_currency, target_currency)

        if result is not None:
            exchange_rate, time_last_update = result

            # Calculate how long ago the exchange rate was updated.
            time_diff = datetime.now() - datetime.fromtimestamp(time_last_update)

            time_ago: str = humanize.naturaltime(time_diff)

            if exchange_rate:
                converted_amount: float = convert_currency(amount, exchange_rate)

                # Display exchange rate information.
                st.success(
                    f"✅ Exchange Rate: {exchange_rate:.4f} "
                    f"(Last updated: {time_ago})"
                )

                # Display conversion results in three columns.
                col1, col2, col3 = st.columns(3)

                col1.metric(
                    label="Base Currency", value=f"{amount:.2f} {base_currency}"
                )

                col2.markdown(
                    """
                    <h1 style='text-align: center; margin: 0;
                    color: green;'>&#8594;</h1>
                    """,
                    unsafe_allow_html=True,
                )

                col3.metric(
                    label="Target Currency",
                    value=f"{converted_amount:.2f} {target_currency}",
                )

            else:
                st.error("Invalid exchange rate received.")

        else:
            st.error("Error fetching exchange rate...")

    # Display application information.
    st.markdown("---")
    st.markdown("### ℹ️ About This Tool")

    st.markdown("""
        This currency converter uses exchange rates provided
        by ExchangeRate-API.

        - The conversion updates automatically as you input
          the amount or change the currency.
        - Enjoy seamless currency conversion without the
          need to press a button!
        """)


if __name__ == "__main__":
    main()
