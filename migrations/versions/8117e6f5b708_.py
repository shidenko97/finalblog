"""empty message

Revision ID: 8117e6f5b708
Revises: 
Create Date: 2020-03-30 16:48:25.156627

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8117e6f5b708'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('fullname', sa.String(length=64), nullable=True),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.Column('sex', sa.String(length=1), nullable=True),
    sa.Column('password', sa.String(length=64), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('user_role',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ondelete='CASCADE', ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE', )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_role')
    op.drop_table('user')
    op.drop_table('role')
    # ### end Alembic commands ###
