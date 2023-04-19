"""empty message

Revision ID: 9ca97299e84a
Revises: 80937f5d195f
Create Date: 2023-04-17 19:45:48.241399

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ca97299e84a'
down_revision = '80937f5d195f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('like',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('like')
    # ### end Alembic commands ###