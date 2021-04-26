from flask_login import UserMixin, LoginManager, current_user, login_user, login_required
from flask import Flask, request, render_template, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import json
from flask_login import UserMixin
db=SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    myRecipes = db.relationship('UserRecipe', backref='user_recipe', lazy=True)

    def toDict(self):
        return {
        "id": self.id,
        "username": self.username,
        "email": self.email,
        "password": self.password
      }

    #hashes the password parameter and stores it in the object
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    #Returns true if the parameter is equal to the object’s password property
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    #To String method
    def __repr__(self):
        return '<User {}>'.format(self.username)

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    count = db.Column(db.Integer)
    def toDict(self):
        return{
            "id": self.id,
            "name": self.name,
            "count": self.count
        }

    def amount(self):
        return self.count

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    ingredients_list = db.Column(db.String(1000))
    instructions = db.Column(db.String(5000))
    recipes = db.relationship('UserRecipe', backref='userrecipe', lazy=True)

    def toDict(self):
        return{
            "id": self.id,
            "name": self.name,
            "ingredients": self.ingredients_list,
            "instructions": self.instructions
        }

class UserRecipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipeID = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    ingredients_list = db.Column(db.String(1000))
    name = db.Column(db.String(50))
    def toDict(self):
        return {
            "id": self.id,
            "userID": self.userID,
            "recipeID": self.recipeID
        }