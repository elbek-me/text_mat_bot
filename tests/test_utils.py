from app.utils import split_message


def test_short_text_is_single_chunk():
    assert split_message("salom", 100) == ["salom"]


def test_long_text_is_split_within_limit():
    text = " ".join(["so'z"] * 2000)
    chunks = split_message(text, 500)
    assert len(chunks) > 1
    assert all(len(c) <= 500 for c in chunks)
    assert " ".join(chunks).split() == text.split()


def test_text_without_spaces_is_hard_split():
    chunks = split_message("a" * 1050, 500)
    assert [len(c) for c in chunks] == [500, 500, 50]
