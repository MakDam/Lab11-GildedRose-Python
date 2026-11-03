"""Рефакторированная реализация Gilded Rose.

Поведение соответствует классическим правилам учебной каты:
- обычные товары теряют 1 качество за день, после срока — 2;
- Aged Brie улучшается на 1, после срока — на 2;
- Backstage passes улучшаются на 1/2/3 в зависимости от срока
  и обнуляются после концерта;
- Sulfuras не меняет качество и срок;
- качество обычных товаров и Aged Brie находится в диапазоне 0..50.
"""

from dataclasses import dataclass

MAX_QUALITY = 50
MIN_QUALITY = 0
EXPIRED_QUALITY_CHANGE = 2
NORMAL_QUALITY_CHANGE = 1

AGED_BRIE = "Aged Brie"
SULFURAS = "Sulfuras, Hand of Ragnaros"
BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"


@dataclass
class Item:
    """Товар магазина."""

    name: str
    sell_in: int
    quality: int

    def __str__(self) -> str:
        return f"{self.name}, {self.sell_in}, {self.quality}"


class GildedRose:
    """Обновляет состояние всех товаров на один день."""

    def __init__(self, items: list[Item]):
        self.items = items

    def update_quality(self) -> None:
        """Обновить срок продажи и качество каждого товара."""
        for item in self.items:
            if item.name == SULFURAS:
                continue

            if item.name == AGED_BRIE:
                self._update_aged_brie(item)
            elif item.name == BACKSTAGE_PASSES:
                self._update_backstage_passes(item)
            else:
                self._update_normal_item(item)

    @staticmethod
    def _update_aged_brie(item: Item) -> None:
        """Сыр улучшается со временем, но не выше максимума."""
        change = EXPIRED_QUALITY_CHANGE if item.sell_in <= 0 else NORMAL_QUALITY_CHANGE
        item.quality = min(MAX_QUALITY, item.quality + change)
        item.sell_in -= 1

    @staticmethod
    def _update_backstage_passes(item: Item) -> None:
        """Билеты дорожают по мере приближения концерта."""
        if item.sell_in <= 0:
            item.quality = MIN_QUALITY
        elif item.sell_in <= 5:
            item.quality = min(MAX_QUALITY, item.quality + 3)
        elif item.sell_in <= 10:
            item.quality = min(MAX_QUALITY, item.quality + 2)
        else:
            item.quality = min(MAX_QUALITY, item.quality + 1)

        item.sell_in -= 1

    @staticmethod
    def _update_normal_item(item: Item) -> None:
        """Обычный товар теряет качество; после срока — быстрее."""
        change = EXPIRED_QUALITY_CHANGE if item.sell_in <= 0 else NORMAL_QUALITY_CHANGE
        item.quality = max(MIN_QUALITY, item.quality - change)
        item.sell_in -= 1
