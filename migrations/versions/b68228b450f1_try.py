"""try

Revision ID: b68228b450f1
Revises: cc91b38ce1dd
Create Date: 2020-04-22 15:06:07.432309

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b68228b450f1'
down_revision = 'cc91b38ce1dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'students', type_='foreignkey')
    op.create_foreign_key(None, 'students', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(None, 'teachers', type_='foreignkey')
    op.create_foreign_key(None, 'teachers', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.alter_column('users_words', 'status',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users_words', 'status',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_constraint(None, 'teachers', type_='foreignkey')
    op.create_foreign_key(None, 'teachers', 'users', ['user_id'], ['id'])
    op.drop_constraint(None, 'students', type_='foreignkey')
    op.create_foreign_key(None, 'students', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###
