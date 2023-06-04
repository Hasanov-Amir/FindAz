"""empty message

Revision ID: 902c675b488f
Revises: 61451a55bb0b
Create Date: 2023-06-04 01:45:26.514112

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '902c675b488f'
down_revision = '61451a55bb0b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('title', sa.String(length=30), nullable=True),
    sa.Column('owner', sa.String(length=50), nullable=True),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.Column('properties', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('create_date', postgresql.TIMESTAMP(), nullable=True),
    sa.Column('edit_date', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('findaz')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('findaz',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('create_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('edit_date', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('title', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('owner', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('count', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('properties', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='findaz_pkey')
    )
    op.drop_table('product')
    # ### end Alembic commands ###
