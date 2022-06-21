from collections import namedtuple

RoleTuple = namedtuple("Role", "name id")


class Roles:
    administrator = RoleTuple("administrator", "00000000-0000-0000-0000-000000000003")
    exporter = RoleTuple("exporter", "00000000-0000-0000-0000-000000000004")
    agent = RoleTuple("agent", "00000000-0000-0000-0000-000000000005")
    immutable_roles = [administrator, exporter, agent]
