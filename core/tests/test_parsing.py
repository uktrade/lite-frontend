from core.parsing import parse_boolean


def test_parse_boolean():
    assert parse_boolean(True) == True
    assert parse_boolean(False) == False
    assert parse_boolean("yes") == True
    assert parse_boolean("no") == False
    assert parse_boolean("YES") == True
    assert parse_boolean("NO") == False
    assert parse_boolean("true") == True
    assert parse_boolean("false") == False
