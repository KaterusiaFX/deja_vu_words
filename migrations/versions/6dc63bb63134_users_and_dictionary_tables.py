"""users and dictionary tables

Revision ID: 6dc63bb63134
Revises: 
Create Date: 2020-04-02 15:19:53.882098

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6dc63bb63134'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('English_words',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('word_itself', sa.String(), nullable=False),
    sa.Column('translation_rus', sa.String(), nullable=False),
    sa.Column('transcription', sa.String(), nullable=True),
    sa.Column('audio_url', sa.String(), nullable=True),
    sa.Column('picture_url', sa.String(), nullable=True),
    sa.Column('imported_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('audio_url'),
    sa.UniqueConstraint('picture_url'),
    sa.UniqueConstraint('word_itself')
    )
    op.create_table('English_words_added_by_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('word_itself', sa.String(), nullable=False),
    sa.Column('user', sa.String(), nullable=False),
    sa.Column('translation_rus', sa.String(), nullable=False),
    sa.Column('transcription', sa.String(), nullable=True),
    sa.Column('audio_url', sa.String(), nullable=True),
    sa.Column('picture_url', sa.String(), nullable=True),
    sa.Column('imported_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('audio_url'),
    sa.UniqueConstraint('picture_url')
    )
    op.create_table('French_words',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('word_itself', sa.String(), nullable=False),
    sa.Column('translation_rus', sa.String(), nullable=False),
    sa.Column('transcription', sa.String(), nullable=True),
    sa.Column('feminine_or_masculine', sa.String(), nullable=True),
    sa.Column('french_verb_group', sa.String(), nullable=True),
    sa.Column('audio_url', sa.String(), nullable=True),
    sa.Column('picture_url', sa.String(), nullable=True),
    sa.Column('imported_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('audio_url'),
    sa.UniqueConstraint('picture_url'),
    sa.UniqueConstraint('word_itself')
    )
    op.create_table('French_words_added_by_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('word_itself', sa.String(), nullable=False),
    sa.Column('user', sa.String(), nullable=False),
    sa.Column('translation_rus', sa.String(), nullable=False),
    sa.Column('transcription', sa.String(), nullable=True),
    sa.Column('feminine_or_masculine', sa.String(), nullable=True),
    sa.Column('french_verb_group', sa.String(), nullable=True),
    sa.Column('audio_url', sa.String(), nullable=True),
    sa.Column('picture_url', sa.String(), nullable=True),
    sa.Column('imported_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('audio_url'),
    sa.UniqueConstraint('picture_url')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('role', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_role'), 'users', ['role'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('users_words',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('engword_id', sa.Integer(), nullable=True),
    sa.Column('frenchword_id', sa.Integer(), nullable=True),
    sa.Column('user_engword_id', sa.Integer(), nullable=True),
    sa.Column('user_frenchword_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['engword_id'], ['English_words.id'], ),
    sa.ForeignKeyConstraint(['frenchword_id'], ['French_words.id'], ),
    sa.ForeignKeyConstraint(['user_engword_id'], ['English_words_added_by_users.id'], ),
    sa.ForeignKeyConstraint(['user_frenchword_id'], ['French_words_added_by_users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_words')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_role'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('French_words_added_by_users')
    op.drop_table('French_words')
    op.drop_table('English_words_added_by_users')
    op.drop_table('English_words')
    # ### end Alembic commands ###
