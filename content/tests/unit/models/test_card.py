import json

import pytest

from content.models import Card
from content.tests.factories.board_factory import BoardFactory


@pytest.mark.django_db
def test_카드를_생성할_수_있다():
    card = Card.objects.create(
        board_id=1,
        no=1,
        description="description",
        meaning="meaning",
        example="example",
        cardSet=1,
        category="category",
        image_front="image_front",
        image_back="image_back",
        front_image_size_w=100,
        front_image_size_h=100,
        back_image_size_w=100,
        back_image_size_h=100,
        zoom_ratio=100,
    )

    assert Card.objects.count() == 1
    assert card.no == 1
    assert card.description == "description"
    assert card.meaning == "meaning"
    assert card.example == "example"
    assert card.cardSet == 1
    assert card.category == "category"
    assert card.image_front == "image_front"
    assert card.image_back == "image_back"
    assert card.front_image_size_w == 100
    assert card.front_image_size_h == 100
    assert card.back_image_size_w == 100
    assert card.back_image_size_h == 100
    assert card.zoom_ratio == 100


@pytest.mark.django_db
def test_json_파일에서_카드를_생성할_수_있다():
    board = BoardFactory()

    board.cards.all().delete()

    assert board.cards.count() == 0

    file_path = "assets/cards.json"
    with open(file_path, "r") as f:
        cards = json.load(f)
        for card in cards:
            Card.objects.create(
                **card,
                board=board,
            )

    assert board.cards.count() == 504
