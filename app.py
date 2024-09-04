from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from forms import RegistrationForm, LoginForm, RecipeForm
from models import db, User, Recipe

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = form.password.data 
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:  
            flash('Login successful!', 'success')
            return redirect(url_for('user_page'))
        else:
            flash('Login failed. Check your username and/or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/user_page')
def user_page():
    user = User.query.first()  
    recipes = Recipe.query.filter_by(author=user).all()
    return render_template('user_page.html', recipes=recipes)

@app.route('/recipe/<int:recipe_id>', methods=['GET', 'POST'])
def recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe.html', recipe=recipe)

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        user = User.query.first()
        new_recipe = Recipe(title=form.title.data, complexity=form.complexity.data,
                            taste=form.taste.data, ingredients=form.ingredients.data,
                            instructions=form.instructions.data, author=user)
        db.session.add(new_recipe)
        db.session.commit()
        flash('Recipe added!', 'success')
        return redirect(url_for('user_page'))
    return render_template('edit_recipe.html', form=form)

@app.route('/edit_recipe/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    form = RecipeForm(obj=recipe)
    if form.validate_on_submit():
        recipe.title = form.title.data
        recipe.complexity = form.complexity.data
        recipe.taste = form.taste.data
        recipe.ingredients = form.ingredients.data
        recipe.instructions = form.instructions.data
        db.session.commit()
        flash('Recipe updated!', 'success')
        return redirect(url_for('recipe', recipe_id=recipe.id))
    return render_template('edit_recipe.html', form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
