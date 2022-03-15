from .requests_helper import post


def create_goods(fixture, headers):
    return post("goods/", {"json": fixture, "headers": headers}).json()


def create_goods_document(good_id, fixture, headers):
    post(f"goods/{good_id}/documents/", {"json": fixture, "headers": headers})
