"""fifth  migration

Revision ID: f4f036eded2a
Revises: 05cd96b4bd73
Create Date: 2024-11-03 23:31:15.898891

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4f036eded2a'
down_revision = '05cd96b4bd73'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('link', schema=None) as batch_op:
        batch_op.add_column(sa.Column('referral_count', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('link', schema=None) as batch_op:
        batch_op.drop_column('referral_count')

    # ### end Alembic commands ###
