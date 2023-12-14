from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL
import pymysql
app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'superSecret'
app.config['MYSQL_DATABASE_DB'] = 'memes'
app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_CURSORCLASS'] = pymysql.cursors.DictCursor
mysql.init_app(app)

# This function will be run whenever requests to "/" are made by the browser.
# The HTML returned from here will be sent to the browser making the request.
@app.route("/")
def index():
    message = "Does this work?"
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM memes ORDER BY RAND() LIMIT 1");
    row = cursor.fetchone()
    if row is None:
        meme_url = "https://media.giphy.com/media/13d2jHlSlxklVe/giphy.gif"
    else:
        meme_url = row["url"]
    return render_template("index.html", message=message, meme_url=meme_url)

@app.route("/add-meme", methods=["POST"])
def add_meme():
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO memes (`url`) VALUES (%s)", request.form["url"])
    db.commit()
    return redirect("/")

# This starts our Python app
if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")