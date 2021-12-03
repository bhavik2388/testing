from flask import Flask, render_template, request
import datetime
from pymongo import MongoClient

def create_app():
 
    app = Flask(__name__)

    client = MongoClient("mongodb+srv://Anuj:Anuj123@cluster0.myrej.mongodb.net/test")

    app.db = client.Microblog    

    entries = []

    @app.route("/", methods = ["GET","POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")  #content is the name of the html field (request.form behaves like a dictionary)4

            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")

            entries.append((entry_content, formatted_date))

            app.db.entries.insert_one({"content" : entry_content, "date" : formatted_date})

        enteries_with_date = [
                (
                    entry["content"],
                    entry["date"],
                    datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")

                )

                for entry in app.db.entries.find({})
            ]
            

        return render_template("home.html", entries = enteries_with_date)

    return app