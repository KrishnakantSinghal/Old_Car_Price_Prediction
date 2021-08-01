import numpy as np
from flask import Flask, request, render_template
import joblib
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

model = joblib.load('C:\\codes\\ML Projects\\Car Price Prediction\\ucpp_model')

# Creating Database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todolist.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    Name = db.Column(db.String(200), nullable = False)
    Location = db.Column(db.String(100), nullable = False)
    Year = db.Column(db.Integer, nullable = False)
    kilometers_Driven = db.Column(db.Float, nullable = False)
    Fuel_Type = db.Column(db.String(20), nullable = False)
    Transmission_Type = db.Column(db.String(20), nullable = False)
    Number_of_Previous_Owners = db.Column(db.Integer, nullable = False)
    Mileage_kmpl = db.Column(db.Float, nullable = False)
    Engine_Capacity_CC = db.Column(db.Float, nullable = False)
    Power_bph = db.Column(db.Float, nullable = False)
    Number_of_Seats = db.Column(db.Float, nullable = False)
    Price_Predicted = db.Column(db.Float, nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.Name}"

@app.route("/") # this will direct  us to the home page when we click our web app link
def home():
      return render_template("index.html")  # home page
    
@app.route("/predict", methods = ["POST", "GET"]) # this works when the user click the prediction button
def predict():
      name = request.form["name"] # taking name of car input from the user  
      location = request.form["location"] # taking location of selling
      year = int(request.form["year"]) # taking year input from the user
      
      fuel_type = request.form["fuel_type"] # type of fuel of car
      # if loop for assigning numerical values
      if fuel_type == "Petrol":
            fuel_ = 2
            
      elif fuel_type == "CNG":
            fuel_ = 0
    
      elif fuel_type == "Diesel":
            fuel_ = 1

      kms_driven = int(request.form["Kms_Driven"]) # total driven kilometers of the car
      transmission = request.form["Transmission_Manual"] # transmission type
      # assigning numerical values
      if transmission == "Manuel":
            transmission_ = 1
      else:
            transmission_ = 0
    
      owner = int(request.form["Owner"])  # number of owners
      mileage = float(request.form["mileage"]) #mileage in kmpl
      engine = float(request.form["engine"]) # engine capacity in CC
      power = float(request.form["power"]) #T power in bhp
      seats = float(request.form["seats"]) # no. of seats

      values = [[
        year,
        kms_driven,
        fuel_,
        transmission_,
        owner,
        mileage,
        engine,
        power,
        seats
        ]]


      # created a list of all the user inputed values, then using it for prediction
      prediction = model.predict(values)
      prediction = round(prediction[0],2)
      # returning the predicted value inorder to display in the front end web application

      if request.method == 'POST':
            todo = Todo(Name = name, Location = location, Year = year, kilometers_Driven = kms_driven,
            Fuel_Type = fuel_type, Transmission_Type = transmission, Number_of_Previous_Owners = owner,
            Mileage_kmpl = mileage, Engine_Capacity_CC = engine, Power_bph = power, Number_of_Seats = seats, Price_Predicted = prediction)
            db.create_all()
            db.session.add(todo)
            db.session.commit()

      allTodo = Todo.query.all()
      return render_template("index.html", pred = "Car price is {} Lakh".format(float(prediction)))
if __name__ == "__main__":
    app.run(debug = True, port = 5000)