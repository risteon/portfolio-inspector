#!/usr/bin/env python
import datetime
import pathlib

import click
import numpy as np
import pandas as pd
import pyEX
import requests

from portfolio_inspector.data_provider import DataProviderCached, DataProviderIEXCloud


@click.command()
@click.argument("trades", type=click.File("r"))
def main(trades):

    data_provider_iex_cloud = DataProviderIEXCloud()
    data_provider = DataProviderCached(data_provider_iex_cloud)

    xx = pd.read_csv(trades)
    xx.dropna(subset=["Date"], inplace=True)

    isin_unique: np.ndarray = pd.unique(xx["ISIN"])
    print(isin_unique)

    data_provider.lookup_isin(isin_unique[:4])

    quit(0)

    date_start = datetime.date(2021, 8, 3)
    date_end = datetime.date(2021, 8, 25)

    data_provider.get_symbol_meta("AAPL")

    # chart = data_provider.get_chart_day_range("AAPL", date_start, date_end)
    chart = data_provider.get_chart_day_range("AAPL", date_start, date_end)
    # chart = data_provider.get_chart_day_range("GOOGL", date_start, date_end)

    print(chart)


if __name__ == "__main__":
    main()
