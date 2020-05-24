from .base import Base  # noqa

# Import all the models, so that Base has
# them before being imported by Alembic.
from .. import models  # noqa
