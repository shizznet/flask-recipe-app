from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.fields.choices import SelectField
from wtforms.fields.form import FormField
from wtforms.fields.list import FieldList
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired

from app import db
from app.models import models
from config import VIEW_RECIPES


class IngredientForm(FlaskForm):
    title = StringField("Name", validators=[DataRequired()])
    quantity = StringField("Quantity", validators=[DataRequired()])
    measurement_type = SelectField(
        "Measurement Type",
        choices=[
            ("grams", "grams"),
            ("milliliters", "milliliters"),
            ("pieces", "pieces"),
        ],
        render_kw={"class": "browser-default"},
    )


class RecipeForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField(
        "Description",
        validators=[DataRequired()],
        render_kw={"class": "materialize-textarea"},
    )
    instructions = TextAreaField(
        "Instructions",
        validators=[DataRequired()],
        render_kw={"class": "materialize-textarea"},
    )
    ingredients = FieldList(FormField(IngredientForm), min_entries=1)
    submit = SubmitField("Add Recipe")


bp = Blueprint("recipe", __name__)


def generate_breadcrumbs():
    breadcrumbs = [{"url": "/", "text": "Home"}]  # Default breadcrumb for home page

    # Extract the path from the request URL
    path = request.path.strip("/").split("/")

    # Iterate over the path segments and generate breadcrumbs
    url_so_far = "/"
    for segment in path:
        url_so_far += segment + "/"
        breadcrumbs.append(
            {"url": "/" + url_so_far.strip("/"), "text": segment.capitalize()}
        )

    return breadcrumbs


@bp.route("/")
def index():
    recipes = models.Recipe.query.all()
    breadcrumbs = generate_breadcrumbs()
    return render_template("index.html", recipes=recipes, breadcrumbs=breadcrumbs)


@bp.route("/recipe", methods=["GET"])
@login_required
def view_recipes():
    page = request.args.get(
        "page", 1, type=int
    )  # Get the page number from the query string
    search_term = request.args.get("search", "")

    if search_term:
        recipes = (
            models.Recipe.query.join(models.Ingredient)
            .filter(models.Recipe.created_by == current_user.id)
            .filter(
                models.Recipe.title.contains(search_term)
                | models.Ingredient.title.contains(search_term)
            )
            .distinct()
            .paginate(page=page, per_page=10)
        )
    else:
        recipes = models.Recipe.query.filter(
            models.Recipe.created_by == current_user.id
        ).paginate(page=page, per_page=10, error_out=False)

    breadcrumbs = generate_breadcrumbs()
    return render_template(
        "recipes.html",
        recipes=recipes.items,
        pagination=recipes,
        breadcrumbs=breadcrumbs,
        search_term=search_term,
    )


@bp.route("/recipe/add", methods=["GET", "POST"])
@login_required
def add_recipe():
    breadcrumbs = generate_breadcrumbs()
    form = RecipeForm()
    check_form = form.validate_on_submit()
    only_csrf_errors = all(
        len(e) == 1 and "csrf_token" in e for e in form.errors.get("ingredients", [])
    )

    form_metadata = {
        "title": "Recipe Form - Add",
        "description": "Please fill out the form to add a recipe.",
        "submit_text": "Add",
        # Add more metadata as needed
    }

    if request.method == "POST" and (check_form or only_csrf_errors):
        recipe = models.Recipe(
            title=form.title.data,
            description=form.description.data,
            instructions=form.instructions.data,
            created_by=current_user.id,
        )
        for ingredient_data in form.ingredients.data:
            ingredient = models.Ingredient(
                title=ingredient_data["title"],
                quantity=ingredient_data["quantity"],
                measurement_type=ingredient_data["measurement_type"],
            )
            recipe.ingredients.append(ingredient)
        db.session.add(recipe)
        db.session.commit()
        flash("Recipe added successfully!", "success")
        return redirect(url_for(VIEW_RECIPES))
    return render_template(
        "recipe_form.html",
        form=form,
        form_metadata=form_metadata,
        breadcrumbs=breadcrumbs,
    )


@bp.route("/recipe/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_recipe(id):
    breadcrumbs = generate_breadcrumbs()
    recipe = models.Recipe.query.get_or_404(id)
    if recipe.author != current_user:
        flash("You do not have permission to edit this recipe.")
        return redirect(url_for(VIEW_RECIPES))
    form = RecipeForm(obj=recipe)

    form_metadata = {
        "title": "Recipe Form - Edit",
        "description": "Please fill out the form to add a recipe.",
        "submit_text": "Edit",
        # Add more metadata as needed
    }

    if request.method == "POST" and (
        form.validate_on_submit()
        or all(
            len(e) == 1 and "csrf_token" in e
            for e in form.errors.get("ingredients", [])
        )
    ):
        try:
            recipe.title = form.title.data
            recipe.description = form.description.data
            recipe.instructions = form.instructions.data

            # Clear existing ingredients and replace with new ones
            # First, delete existing ingredients from the database
            models.Ingredient.query.filter_by(recipe_id=recipe.id).delete()

            # Then, add new ingredients
            for idx, ingredient_data in enumerate(form.ingredients.data):
                ingredient = models.Ingredient(
                    title=ingredient_data["title"],
                    quantity=ingredient_data["quantity"],
                    measurement_type=ingredient_data["measurement_type"],
                    recipe_id=recipe.id,
                )
                db.session.add(ingredient)

            db.session.commit()
            flash("Your recipe has been updated.")
            return redirect(url_for(VIEW_RECIPES))
        except Exception as e:
            db.session.rollback()  # Roll back the transaction
            flash("An error occurred while updating the recipe.")
            # Log the error or handle it appropriately
            return render_template("error.html", error=str(e))
    return render_template(
        "recipe_form.html",
        form=form,
        recipe=recipe,
        form_metadata=form_metadata,
        breadcrumbs=breadcrumbs,
    )


@bp.route("/recipe/<int:id>/delete", methods=["POST"])
@login_required
def delete_recipe(id):
    recipe = models.Recipe.query.get_or_404(id)
    if recipe.author != current_user:
        flash("You do not have permission to delete this recipe.")
        return redirect(url_for(VIEW_RECIPES))
    try:
        db.session.delete(recipe)
        db.session.commit()
        flash("Your recipe has been deleted.")
    except Exception as e:
        db.session.rollback()  # Roll back the transaction if an error occurs
        # flash("An error occurred while deleting the recipe.")
        # Log the error or handle it appropriately
        print(e)
    return redirect(url_for(VIEW_RECIPES))


@bp.route("/recipe/<int:id>", methods=["GET"])
@login_required
def view_recipe(id):
    breadcrumbs = generate_breadcrumbs()
    recipe = models.Recipe.query.get_or_404(id)
    if recipe.author != current_user:
        flash("You do not have permission to delete this recipe.")
        return redirect(url_for(VIEW_RECIPES))
    return render_template("recipe_view.html", recipe=recipe, breadcrumbs=breadcrumbs)
