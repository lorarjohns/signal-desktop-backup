import yaml
import pytest
from collections import namedtuple


"""Removes leading '+', '#', etc. Also removes emoji, leaving empty strings"""


@pytest.fixture(
    params=[
        ("Christina Axxx-Pxxxx", "Christina_Axxx_Pxxxx", "8f45b56a28ccb64454b02a639220b878"),
        ("Dan Axxxxxx", "Dan_Axxxxxx", "a9334f77b13e0888200781a251f9b249"),
        ("Asher", "Asher", "695051b4ecd7189ca6e5b0544cac4efa"),
        ("Karen Xxxxxx Thinksyourhot<3", "Karen_Xxxxxx_Thinksyourhot", "c64f2efb81df74bc9fd679a95500fabf"),
        ("#BUDS", "BUDS", "f61599852b25f3b775c8836231aec810"),
        ("w4rner", "w4rner", "37888318210f650aa9e2ac5bbeed7485"),
        ("✨🌲", "SPARKLES_EVERGREEN_TREE_", "adbd36232defec9696996bbd574cfb5d"),
        ("+18882703171", "18882703171", "343e73b22751eed29d626d884f2f957d"),
        ("+18885628877", "18885628877", "ec6a7633eaaf078c37a1a59cbcb203b9"),
        ("+18888971646", "18888971646", "1f527caffaf57e6ccaa45662aeb7268b"),
        ("+18888971646", "18888971646", "1f527caffaf57e6ccaa45662aeb7268b"),
        ("+18884446116", "18884446116", "fe23592143e01c035c8948f00a898f66"),
    ]
)
def conversation(request):
    def _get_conversations(record):
        conversation = namedtuple("conversation", "original expected hash")
        return conversation(*record)

    return _get_conversations(request.param)
