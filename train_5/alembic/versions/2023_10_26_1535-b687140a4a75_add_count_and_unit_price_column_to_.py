"""add count and unit_price column to order product association table

Revision ID: b687140a4a75
Revises: 687006201af0
Create Date: 2023-10-26 15:35:56.786930

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b687140a4a75"
down_revision: Union[str, None] = "687006201af0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "order_product_association",
        sa.Column("count", sa.Integer(), server_default="1", nullable=False),
    )
    op.add_column(
        "order_product_association",
        sa.Column("unit_price", sa.Integer(), server_default="1", nullable=False),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("order_product_association", "unit_price")
    op.drop_column("order_product_association", "count")
    # ### end Alembic commands ###