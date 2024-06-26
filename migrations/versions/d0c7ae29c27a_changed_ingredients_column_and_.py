"""Changed ingredients column and converted to a foreign

Revision ID: d0c7ae29c27a
Revises: e66f6d7dfd5f
Create Date: 2024-04-04 10:49:40.693419

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "d0c7ae29c27a"
down_revision = "e66f6d7dfd5f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "ingredient",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("quantity", sa.String(length=50), nullable=False),
        sa.Column("measurement_type", sa.String(length=50), nullable=False),
        sa.Column("recipe_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["recipe_id"],
            ["recipe.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("recipe", schema=None) as batch_op:
        batch_op.alter_column(
            "title",
            existing_type=sa.VARCHAR(length=128),
            type_=sa.String(length=100),
            existing_nullable=False,
        )
        batch_op.alter_column("description", existing_type=sa.TEXT(), nullable=False)
        batch_op.alter_column("instructions", existing_type=sa.TEXT(), nullable=False)
        batch_op.alter_column("created_by", existing_type=sa.INTEGER(), nullable=False)
        batch_op.drop_column("ingredients")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("recipe", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "ingredients",
                postgresql.JSON(astext_type=sa.Text()),
                autoincrement=False,
                nullable=True,
            )
        )
        batch_op.alter_column("created_by", existing_type=sa.INTEGER(), nullable=True)
        batch_op.alter_column("instructions", existing_type=sa.TEXT(), nullable=True)
        batch_op.alter_column("description", existing_type=sa.TEXT(), nullable=True)
        batch_op.alter_column(
            "title",
            existing_type=sa.String(length=100),
            type_=sa.VARCHAR(length=128),
            existing_nullable=False,
        )

    op.drop_table("ingredient")
    # ### end Alembic commands ###
