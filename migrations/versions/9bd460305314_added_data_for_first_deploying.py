"""Added data for first deploying

Revision ID: 9bd460305314
Revises: e1eb555f77e2
Create Date: 2020-04-07 14:32:43.473700

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9bd460305314'
down_revision = 'e1eb555f77e2'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('INSERT INTO role (name) VALUES (\'User\')')


def downgrade():
    op.execute('DELETE FROM role WHERE name = \'User\'')
