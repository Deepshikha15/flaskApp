from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


app = Flask(__name__)

app.config.update(dict(
    SECRET_KEY=" ",
    WTF_CSRF_SECRET_KEY=" "
))


app.config['DEBUG'] = True


# POSTGRES = {
#     'user': 'postgres',
#     'pw': 'z',
#     'db': 'testdb',
#     'host': 'localhost',
#     'port': '5432',
# }

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:z@localhost/testdb'
db = SQLAlchemy(app)




migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)



class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(80), unique=True)
    post_text = db.Column(db.String(255))

    def __init__(self, title, post_text):
        self.title = title
        self.post_text = post_text


@app.route('/addpost', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        post_text = request.form['post_text']

        post = Post(title, post_text)

        db.session.add(post)
        db.session.commit()
        print("updated !! ")
        return redirect(url_for('view_posts'))
    return render_template('post_form.html')



# class PostForm(FlaskForm):
#     title = StringField('Title', validators=[DataRequired()])
#     post_text = StringField('Post_Text', validators=[DataRequired()])
#

# def hello_world():
#     return 'Hello, World!'

# @app.route('/greet')
# def greet():
#     user = {'username': 'John', 'age': "20"}
#     return '''
# <html>
#     <head>
#         <title>Templating</title>
#     </head>
#     <body>
#         <h1>Hello, ''' + user['username'] + '''!, you’re ''' + user['age'] + ''' years old.</h1>
#     </body>
# </html>'''

# @app.route('/hello')
# def hello():
#     return render_template('index.html', name="Alex")

@app.route('/')
def index():
    return "Hello World"



# @app.route('/form', methods=['POST', 'GET'])
# def bio_data_form():
#     if request.method == "POST":
#         username = request.form['username']
#         age = request.form['age']
#         email = request.form['email']
#         hobbies = request.form['hobbies']
#         return redirect(url_for('showbio',
#                                 username=username,
#                                 age=age,
#                                 email=email,
#                                 hobbies=hobbies))
#     return render_template("bio_form.html")
#
#
# @app.route('/showbio', methods=['GET'])
# def showbio():
#     username = request.args.get('username')
#     age = request.args.get('age')
#     email = request.args.get('email')
#     hobbies = request.args.get('hobbies')
#     return render_template("show_bio.html",
#                            username=username,
#                            age=age,
#                            email=email,
#                            hobbies=hobbies)




# @app.route('/addpost', methods=['GET', 'POST'])
# def add_post():
#     postform = PostForm()
#     if request.method == 'POST':
#         pf = Post(
#             postform.title.data,
#             postform.post_text.data,
#         )
#         db.session.add(pf)
#         db.session.commit()
#         return redirect(url_for('view_posts'))
#     return render_template('post_form.html', postform=postform)


@app.route('/posts', methods=['GET', 'POST'])
def view_posts():
    posts = Post.query.all()

    return render_template('view_posts.html', posts=posts)





if __name__ =="__main__":
    manager.run()