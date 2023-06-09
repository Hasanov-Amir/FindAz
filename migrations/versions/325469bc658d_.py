"""empty message

Revision ID: 325469bc658d
Revises: 9e588f4e1769
Create Date: 2023-06-26 21:13:07.061553

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '325469bc658d'
down_revision = '9e588f4e1769'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('product_owner_shop', sa.UUID(), nullable=True))
        batch_op.add_column(sa.Column('product_owner_shop_title', sa.String(length=50), nullable=True))
        batch_op.drop_column('product_owner')

    with op.batch_alter_table('shop', schema=None) as batch_op:
        batch_op.add_column(sa.Column('shop_producr_count', sa.SmallInteger(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('shop', schema=None) as batch_op:
        batch_op.drop_column('shop_producr_count')

    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('product_owner', sa.UUID(), autoincrement=False, nullable=True))
        batch_op.drop_column('product_owner_shop_title')
        batch_op.drop_column('product_owner_shop')

    # ### end Alembic commands ###
