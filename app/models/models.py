from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(255))

    # Relationship to the Recipe model
    recipes = db.relationship("Recipe", backref="author", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(50), nullable=False)
    measurement_type = db.Column(db.String(50), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), nullable=False)

    def __repr__(self):
        return (
            f"Ingredient(name='{self.title}', "
            f"quantity='{self.quantity}', "
            f"measurement_type='{self.measurement_type}')"
        )


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    ingredients = db.relationship(
        "Ingredient", backref="recipe", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"Recipe(title='{self.title}', description='{self.description}', "
            f"instructions='{self.instructions}')"
        )
