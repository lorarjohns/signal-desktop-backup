import yaml
import pytest
from collections import namedtuple


"""Removes leading '+', '#', etc. Also removes emoji, leaving empty strings"""


@pytest.fixture(
    params=[
        ("Christina Axxx-Pxxxx", "Christina_Axxx_Pxxxx"),
        ("Dan Axxxxxx", "Dan_Axxxxxx"),
        ("Asher", "Asher"),
        ("Karen Xxxxxx Thinksyourhot<3", "Karen_Xxxxxx_Thinksyourhot"),
        ("#BUDS", "BUDS"),
        ("w4rner", "w4rner"),
        ("✨🌲", "SPARKLES_EVERGREEN TREE_"),
        ("+18882703171", "18882703171"),
        ("+18885628877", "18885628877"),
        ("+18888971646", "18888971646"),
        ("+18888971646", "18888971646"),
        ("+18884446116", "18884446116"),
    ]
)
def conversation(request):
    def _get_conversations(record):
        conversation = namedtuple("conversation", "original expected")
        return conversation(*record)

    return _get_conversations(request.param)
