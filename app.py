from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SECRET_KEY"] = "softwareslyk"

db = SQLAlchemy(app)

# Database model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/blog")
def blog():
    posts = Post.query.all()
    return render_template("blog.html", posts=posts)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "1234":
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        post = Post(
            title=request.form["title"],
            content=request.form["content"]
        )
        db.session.add(post)
        db.session.commit()
        return redirect("/blog")
    return render_template("create_post.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
