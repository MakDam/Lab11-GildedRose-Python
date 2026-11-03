"""Небольшой запуск программы для проверки в PyCharm."""

from gilded_rose import AGED_BRIE, BACKSTAGE_PASSES, SULFURAS, GildedRose, Item


def main():
    items = [
        Item("+5 Dexterity Vest", 10, 20),
        Item(AGED_BRIE, 2, 0),
        Item(SULFURAS, 0, 80),
        Item(BACKSTAGE_PASSES, 15, 20),
    ]

    shop = GildedRose(items)

    print("До обновления:")
    for item in items:
        print(item)

    shop.update_quality()

    print("\\nПосле обновления:")
    for item in items:
        print(item)


if __name__ == "__main__":
    main()
