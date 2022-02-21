from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField

## Delete this code:
# import requests
# posts = requests.get("https://api.npoint.io/43644ec4f0013682fc0d").json()

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title :", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


@app.route('/')
def get_all_posts():
    blogs = db.session.query(BlogPost).all()

    return render_template("index.html", all_posts=blogs)


@app.route("/post/<int:index>", methods=['GET'])
def show_post(index):
    post = db.session.query(BlogPost).filter_by(id=index).first()
    return render_template("post.html", post=post)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/edit<int:post_id>", methods=['GET', 'POST'])
def edit_post(post_id):
    q = db.session.query(BlogPost).filter_by(id=post_id).first()
    print(q.title)

    if request.method == 'GET':

        form = CreatePostForm(
            title=q.title,
            subtitle=q.subtitle,
            author=q.author,
            img_url=q.img_url,
            body=q.body

        )

        return render_template("make-post.html", form=form, post_id=post_id)
    elif request.method == 'POST':

        q.title = request.form.get('title')
        q.subtitle = request.form.get('subtitle')
        q.author = request.form.get('author')
        q.img_url = request.form.get('img_url')
        q.body = request.form.get('body')


        db.session.commit()

        return redirect(url_for("get_all_posts"))


if __name__ == "__main__":
    app.run(port=9004)
