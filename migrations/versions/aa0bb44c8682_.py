"""empty message

Revision ID: aa0bb44c8682
Revises: 325469bc658d
Create Date: 2023-07-04 21:16:07.453240

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa0bb44c8682'
down_revision = '325469bc658d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('shop', schema=None) as batch_op:
        batch_op.add_column(sa.Column('shop_product_count', sa.SmallInteger(), nullable=True))
        batch_op.drop_column('shop_producr_count')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('shop', schema=None) as batch_op:
        batch_op.add_column(sa.Column('shop_producr_count', sa.SMALLINT(), autoincrement=False, nullable=True))
        batch_op.drop_column('shop_product_count')

    # ### end Alembic commands ###
