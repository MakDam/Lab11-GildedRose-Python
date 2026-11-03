import pytest

from gilded_rose import (
    AGED_BRIE,
    BACKSTAGE_PASSES,
    SULFURAS,
    GildedRose,
    Item,
)


def update(item):
    GildedRose([item]).update_quality()
    return item


def test_normal_item_loses_one_quality_before_expiration():
    item = update(Item("普通 item", 5, 10))
    assert (item.sell_in, item.quality) == (4, 9)


def test_normal_item_loses_two_quality_after_expiration():
    item = update(Item("Elixir", 0, 10))
    assert (item.sell_in, item.quality) == (-1, 8)


def test_normal_item_quality_never_below_zero():
    item = update(Item("Elixir", 0, 1))
    assert item.quality == 0


def test_aged_brie_increases_quality_before_expiration():
    item = update(Item(AGED_BRIE, 5, 10))
    assert (item.sell_in, item.quality) == (4, 11)


def test_aged_brie_increases_twice_after_expiration():
    item = update(Item(AGED_BRIE, 0, 10))
    assert (item.sell_in, item.quality) == (-1, 12)


def test_aged_brie_quality_never_above_fifty():
    item = update(Item(AGED_BRIE, 5, 50))
    assert item.quality == 50


def test_sulfuras_never_changes():
    item = update(Item(SULFURAS, 0, 80))
    assert (item.sell_in, item.quality) == (0, 80)


@pytest.mark.parametrize(
    "sell_in, expected_quality",
    [(11, 11), (10, 12), (6, 12), (5, 13), (1, 13)],
)
def test_backstage_passes_increase_by_time_to_concert(sell_in, expected_quality):
    item = update(Item(BACKSTAGE_PASSES, sell_in, 10))
    assert item.quality == expected_quality
    assert item.sell_in == sell_in - 1


def test_backstage_passes_drop_to_zero_after_concert():
    item = update(Item(BACKSTAGE_PASSES, 0, 30))
    assert (item.sell_in, item.quality) == (-1, 0)


def test_backstage_passes_quality_never_above_fifty():
    item = update(Item(BACKSTAGE_PASSES, 5, 49))
    assert item.quality == 50


def test_all_items_are_updated_in_one_call():
    items = [
        Item("Elixir", 5, 10),
        Item(AGED_BRIE, 5, 10),
        Item(SULFURAS, 0, 80),
    ]
    GildedRose(items).update_quality()
    assert [(x.sell_in, x.quality) for x in items] == [
        (4, 9), (4, 11), (0, 80)
    ]
