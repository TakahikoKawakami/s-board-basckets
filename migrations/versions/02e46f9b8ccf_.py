"""empty message

Revision ID: 02e46f9b8ccf
Revises: 4786333a7a02
Create Date: 2021-01-17 17:11:49.692419

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02e46f9b8ccf'
down_revision = '4786333a7a02'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('baskets')
    op.add_column('accounts', sa.Column('access_token', sa.Unicode(length=128), nullable=True))
    op.add_column('accounts', sa.Column('expiration_date_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('accounts', 'expiration_date_time')
    op.drop_column('accounts', 'access_token')
    op.create_table('baskets',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('contract_id', sa.VARCHAR(length=32), nullable=False),
    sa.Column('transaction_date', sa.DATETIME(), nullable=False),
    sa.Column('analyze_result', sa.TEXT(), nullable=False),
    sa.Column('analyze_condition', sa.TEXT(), nullable=True),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('modified_at', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
