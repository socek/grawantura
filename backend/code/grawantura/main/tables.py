from typing import Any

from qq.finder import ObjectFinder
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.schema import MetaData

# Recommended naming convention used by Alembic, as various different database
# providers will autogenerate vastly different names making migrations more
# difficult. See: http://alembic.zzzcomputing.com/en/latest/naming.html
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
metadata = MetaData(naming_convention=NAMING_CONVENTION)


class Base:
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def _asdict(self):
        data = dict(self.__dict__)
        del data["_sa_instance_state"]
        return data


class TableFinder(ObjectFinder):
    def is_collectable(self, element: Any) -> bool:
        try:
            return issubclass(element, SqlTable) and element != SqlTable
        except TypeError:
            return False


SqlTable = declarative_base(cls=Base, metadata=metadata)
