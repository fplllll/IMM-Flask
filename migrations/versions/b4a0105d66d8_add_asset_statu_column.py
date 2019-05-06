"""add asset statu column

Revision ID: b4a0105d66d8
Revises: 7b83509f58a4
Create Date: 2019-05-06 19:18:56.451723

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from models.models import Asset


# revision identifiers, used by Alembic.
revision = 'b4a0105d66d8'
down_revision = '7b83509f58a4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bearing', sa.Column('statu', sqlalchemy_utils.types.choice.ChoiceType(Asset.STATUS), nullable=True))
    op.add_column('motor', sa.Column('statu', sqlalchemy_utils.types.choice.ChoiceType(Asset.STATUS), nullable=True))
    op.add_column('rotor', sa.Column('statu', sqlalchemy_utils.types.choice.ChoiceType(Asset.STATUS), nullable=True))
    op.add_column('stator', sa.Column('statu', sqlalchemy_utils.types.choice.ChoiceType(Asset.STATUS), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('stator', 'statu')
    op.drop_column('rotor', 'statu')
    op.drop_column('motor', 'statu')
    op.drop_column('bearing', 'statu')
    # ### end Alembic commands ###