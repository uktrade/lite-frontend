from exporter.goods.forms import GoodArchiveForm, GoodRestoreForm


def test_archive_good_form():
    form = GoodArchiveForm(data={}, cancel_url="")
    assert form.is_valid() is True
    assert form.errors == {}


def test_restore_good_form():
    form = GoodRestoreForm(data={}, cancel_url="")
    assert form.is_valid() is True
    assert form.errors == {}
