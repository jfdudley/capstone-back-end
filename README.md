# DIY Skincare App: Back-end Layer

This app was created as a Capstone project for Ada Developer Academy Cohort 17. The purpose of the app is track skincare recipes, molds for forming solid products, and adjust recipe ingredient amounts based on users' mold selections. It was designed to assist my own hobby of making skincare products. This repository holds the code for the back end database logic. 

## Feature Set

### Database Models
Models include:
- Mold
- Category (one to many relationship with Recipe)
- Location (one to many relationship with Recipe)
- Ingredient
- Recipe
- Recipe-Ingredients (many to many with Recipe and Ingredient)

### API
A Flask based API for most CRUD routes of all models. Certain model instances (Category, Location, Ingredient) are primarily created through creation of a new Recipe instance. 

### Test Suite
Repository includes a full test suite for API routes. 

## Dependencies
The DIY Skincare App relies on:

- Flask
- SQLAlchemy
- postgres
- pytest
- etc (see requirements.txt file)

## Environment Set-up

### Virtual Environment
This code is designed to be run in a virtual environment on a local machine. After forking and/or cloning the repository, be sure to create a virtual environment before installing all requirements in the requirements.txt file. 

### .env File
To run the Flask server locally, create regular and test databases on your local machine. Then add a .env file, and set the `SQLALCHEMY_DATABASE_URI` and `SQLALCHEMY_TEST_DATABASE_URI` values to those database locations for local storage. 

### Heroku Database
This code is deployed on Heroku. Any major updates to this repository should be duplicated in the deployed version. 


