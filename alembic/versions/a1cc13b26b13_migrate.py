"""Migrate

Revision ID: a1cc13b26b13
Revises: 7ea9b7cc933b
Create Date: 2023-05-28 20:46:53.663623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1cc13b26b13'
down_revision = '7ea9b7cc933b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pd_calendar',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=False),
    sa.Column('block_color', sa.String(length=7), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('default', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['pd_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pd_user_settings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('values', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['pd_user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('pd_event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('place', sa.String(length=100), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('duration', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=100), nullable=False),
    sa.Column('block_color', sa.String(length=7), nullable=False),
    sa.Column('organizer_id', sa.Integer(), nullable=False),
    sa.Column('calendar_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['calendar_id'], ['pd_calendar.id'], ),
    sa.ForeignKeyConstraint(['organizer_id'], ['pd_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pd_reoccurring_event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('place', sa.String(length=100), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('duration', sa.Integer(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=False),
    sa.Column('description', sa.String(length=100), nullable=False),
    sa.Column('block_color', sa.String(length=7), nullable=False),
    sa.Column('loop_type', sa.Enum('DAILY', 'WEEKLY', 'MONTHLY', 'MONTHLY_FIRST', 'MONTHLY_SECOND', 'MONTHLY_THIRD', 'MONTHLY_FOURTH', 'MONTHLY_LAST', 'YEARLY', name='looptype'), nullable=False),
    sa.Column('loop_period', sa.Integer(), nullable=False),
    sa.Column('monday', sa.Boolean(), nullable=True),
    sa.Column('tuesday', sa.Boolean(), nullable=True),
    sa.Column('wednesday', sa.Boolean(), nullable=True),
    sa.Column('thursday', sa.Boolean(), nullable=True),
    sa.Column('friday', sa.Boolean(), nullable=True),
    sa.Column('saturday', sa.Boolean(), nullable=True),
    sa.Column('sunday', sa.Boolean(), nullable=True),
    sa.Column('day_of_month', sa.Integer(), nullable=True),
    sa.Column('month_of_year', sa.Integer(), nullable=True),
    sa.Column('organizer_id', sa.Integer(), nullable=False),
    sa.Column('calendar_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['calendar_id'], ['pd_calendar.id'], ),
    sa.ForeignKeyConstraint(['organizer_id'], ['pd_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pd_share_file_user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('file_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('read', sa.Boolean(), nullable=True),
    sa.Column('write', sa.Boolean(), nullable=True),
    sa.Column('delete', sa.Boolean(), nullable=True),
    sa.Column('share', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['file_id'], ['pd_file.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['pd_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pd_share_file_user')
    op.drop_table('pd_reoccurring_event')
    op.drop_table('pd_event')
    op.drop_table('pd_user_settings')
    op.drop_table('pd_calendar')
    # ### end Alembic commands ###
