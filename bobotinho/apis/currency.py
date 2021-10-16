# -*- coding: utf-8 -*-
from coinapi_rest_v1.restapi import CoinAPIv1

from bobotinho import config


class Currency:
    @staticmethod
    def convert(base: str, target: str) -> float:
        return (
            CoinAPIv1(config.currency_key)
            .exchange_rates_get_specific_rate(base.upper(), target.upper())
            .get("rate")
        )
