"""empty message

Revision ID: 9e588f4e1769
Revises: 4d4ceae06dfa
Create Date: 2023-06-21 01:22:54.551833

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9e588f4e1769'
down_revision = '4d4ceae06dfa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('product_title', sa.String(length=30), nullable=True))
        batch_op.add_column(sa.Column('product_owner', sa.UUID(), nullable=True))
        batch_op.add_column(sa.Column('product_count', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('product_properties', postgresql.JSON(astext_type=sa.Text()), nullable=True))
        batch_op.add_column(sa.Column('product_images', postgresql.JSON(astext_type=sa.Text()), nullable=True))
        batch_op.drop_column('owner')
        batch_op.drop_column('count')
        batch_op.drop_column('properties')
        batch_op.drop_column('images')
        batch_op.drop_column('title')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.VARCHAR(length=30), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('images', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('properties', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('count', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('owner', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
        batch_op.drop_column('product_images')
        batch_op.drop_column('product_properties')
        batch_op.drop_column('product_count')
        batch_op.drop_column('product_owner')
        batch_op.drop_column('product_title')

    # ### end Alembic commands ###
