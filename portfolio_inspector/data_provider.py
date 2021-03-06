#!/usr/bin/env python

import datetime
import logging
import pathlib

import numpy as np
import pandas as pd
import pyEX

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(module)s - %(message)s"
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
logger.addHandler(handler)


class DataProviderIEXCloud:
    def __init__(self):
        self._version = "sandbox"
        self._client = pyEX.Client(version=self._version)

    def __repr__(self):
        return f"iexcloud_{self._version}"

    def get_symbol_meta(self, symbol: str):
        print(symbol)
        self._client
        raise NotImplementedError()

    def lookup_isin(self, isin: str) -> pd.DataFrame:
        return self._client.isinLookupDF(isin)

    def get_chart_day_range(self, symbol, date_start: datetime.date) -> pd.DataFrame:
        chart = self._client.chartDF(
            symbol=symbol, closeOnly=True, last=7, timeframe="5y"
        )
        return chart


class DataProviderCached:
    def __init__(
        self, data_provider: DataProviderIEXCloud, cache_location: pathlib.Path = None
    ):
        self._data_provider = data_provider

        if cache_location is None:
            self.cache_location = DataProviderCached.get_default_cache_location()
        else:
            self.cache_location = cache_location

        self.cache_location /= repr(self._data_provider)

        if not self.cache_location.is_dir():
            self.cache_location.mkdir(parents=True)

    @staticmethod
    def get_default_cache_location() -> pathlib.Path:
        cache_location = pathlib.Path.home() / ".cache"
        if not cache_location.is_dir():
            raise RuntimeError("User cache folder unavailable.")
        cache_location /= "portfolio-inspector"
        return cache_location

    def get_symbol_meta(self, symbol: str):
        return self._data_provider.get_symbol_meta(symbol)

    def lookup_isin(self, isin: np.ndarray):
        cache_file = self.cache_location / "isin_symbol.pd"

        try:
            mapping: pd.DataFrame = pd.read_parquet(cache_file)
            # check which isin are already available in mapping
            available = mapping.index.levels[0].values
            missing = list(set(isin) - set(available))

        except FileNotFoundError:
            missing = isin

        if missing:
            isin_symbols = [self._data_provider.lookup_isin(x) for x in missing]
            mapping_update = pd.concat(dict(zip(missing, isin_symbols)))
            mapping = pd.concat((mapping, mapping_update))
            mapping.to_parquet(cache_file)

        return mapping

    def get_chart_day_range(
        self, symbol: str, date_start: datetime.date, date_end: datetime.date
    ):
        cache_file = self.cache_location / f"chart_{symbol}.pd"
        try:
            chart = pd.read_parquet(cache_file)
            logger.info(f"Loaded from cache {str(cache_file)}.")
        except FileNotFoundError:
            chart = self._data_provider.get_chart_day_range(symbol, date_start)
            chart = chart[["close", "volume"]]
            chart.to_parquet(cache_file)

        return chart
