"""Updated settlements column to  installments

Revision ID: 5c6acf8e584f
Revises: c0ed1e338454
Create Date: 2024-09-09 19:30:23.579762

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c6acf8e584f'
down_revision: Union[str, None] = 'c0ed1e338454'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('promotions', sa.Column('installments', sa.Numeric(precision=10, scale=2), nullable=False))
    op.drop_column('promotions', 'settlements')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('promotions', sa.Column('settlements', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=False))
    op.drop_column('promotions', 'installments')
    # ### end Alembic commands ###