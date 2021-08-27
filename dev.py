#!/usr/bin/env python
import datetime
import pathlib

import click
import pyEX
import requests

from portfolio_inspector.data_provider import DataProviderCached, DataProviderIEXCloud


@click.command()
def main():

    data_provider_iex_cloud = DataProviderIEXCloud()
    data_provider = DataProviderCached(data_provider_iex_cloud)

    date_start = datetime.date(2021, 8, 3)
    date_end = datetime.date(2021, 8, 25)

    # chart = data_provider.get_chart_day_range("AAPL", date_start, date_end)
    chart = data_provider.get_chart_day_range("GOOGL", date_start, date_end)

    print(chart)


if __name__ == "__main__":
    main()
