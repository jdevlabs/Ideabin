"""

Updates to Users

Revision ID: 342e8c935de

Revises: 220e35d329b

Create Date: 2014-11-02 13:47:18.303776

"""

# revision identifiers, used by Alembic.

revision = '342e8c935de'

down_revision = '220e35d329b'



from alembic import op

import sqlalchemy as sa

from sqlalchemy.dialects import mysql

def upgrade():

    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('facebook_url', sa.String(length=512), nullable=False, server_default=''))
    op.add_column('user', sa.Column('github_url', sa.String(length=512), nullable=False, server_default=''))
    op.add_column('user', sa.Column('twitter_url', sa.String(length=512), nullable=False, server_default=''))
    op.add_column('user', sa.Column('role', sa.String(length=32), nullable=False, server_default='Noob'))
    op.drop_column('user', 'profile_twitter')
    op.drop_column('user', 'profile_fb')
    ### end Alembic commands ###



def downgrade():

    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('profile_fb', mysql.VARCHAR(collation='utf32_unicode_ci', length=120), nullable=True))
    op.add_column('user', sa.Column('profile_twitter', mysql.VARCHAR(collation='utf32_unicode_ci', length=120), nullable=True))
    op.drop_column('user', 'role')
    op.drop_column('user', 'twitter_url')
    op.drop_column('user', 'github_url')
    op.drop_column('user', 'facebook_url')
    ### end Alembic commands ###

