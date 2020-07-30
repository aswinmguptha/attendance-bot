#!/usr/bin/env python
# -*- coding: utf-8 -*-


from math import ceil
from typing import List, Union
from telegram import (
    ParseMode,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text


def get_time_zone_ntb(page_n: int):
    modules = [
        EqInlineKeyboardButton(
            x,
            callback_data="tz_{}_{}".format(
                page_n,
                x
            )
        ) for x in w_get_btns(page_n)
    ]
    print(modules)

    pairs = list(zip(
        modules[::3],
        modules[1::3],
        modules[2::3]
    ))
    print(pairs)

    if len(modules) % 3 == 1:
        pairs.append((modules[-1],))
    print(pairs)

    max_num_pages = ceil(len(pairs) / 3)
    if max_num_pages > 7:
        modulo_page = page_n % max_num_pages

        # can only have a certain amount of buttons side by side
        if len(pairs) > 7:
            pairs = pairs[
                modulo_page * 7:7 * (modulo_page + 1)
            ] + [(
                EqInlineKeyboardButton(
                    "<",
                    callback_data="{}_prev({})".format(
                        "tz_page", modulo_page
                    )
                ),
                EqInlineKeyboardButton(
                    ">",
                    callback_data="{}_next({})".format(
                        "tz_page", modulo_page
                    )
                )
            )]
    
    print(pairs)
    return InlineKeyboardMarkup(pairs)


def w_get_btns(page_n: int) -> List[Union[int, str]]:
    if page_n == 0:
        return ["👈", "➖", "➕"]
    if page_n == 1:
        return range(0, 12)
    if page_n == 2:
        return range(0, 60)
