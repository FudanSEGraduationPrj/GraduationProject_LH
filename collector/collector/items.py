# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class JavaDescriptionItem(Item):
    keyword = Field()
    description = Field()


class WikiUrlItem(Item):
    url = Field()


class WikiParaItem(Item):
    text = Field()
    is_explanation = Field()


class StackOverflowAnswerItem(Item):
    answer = Field()
