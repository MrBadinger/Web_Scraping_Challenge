# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# create route that renders index.html template
@app.route("/")
def index():
    mars_db = mongo.db.mars_db.find_one()
    return render_template("index.html", mars=mars_db)

@app.route("/scrape")
def scrape():

    mars_db = mongo.db.mars_db
    mars_data = scrape_mars.scrape()
    mars_db.insert_one(mars_data)
    mars_db.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)