from flask import Flask, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_migrate import Migrate
from forms import SearchForm, CreateResourceForm, CommentForm
from flask_ckeditor import CKEditor


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBfqeuibnvuiguosdk139r93b'


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resources.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)
ckeditor = CKEditor(app)
migrate = Migrate(app, db)


class Resources(db.Model):
    __tablename__ = "resources"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    # Parent relationship to the reviews
    reviews = relationship('Reviews', back_populates='parent_resource')


class Reviews(db.Model):
    __tablename__ = "reviews"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    # Child relationship to the Resources
    resource_id: Mapped[str] = mapped_column(Integer, db.ForeignKey("resources.id"))
    parent_resource = relationship('Resources', back_populates='reviews')


@app.route('/', methods=['get', 'post'])
def home():
    form = SearchForm()
    if form.validate_on_submit():
        search_word = form.search.data
        query_result = set(Resources.query.filter(Resources.name.like(f'%{search_word}%')).all())
        query_result.update(Resources.query.filter(Reviews.content.like(f'%{search_word}%')).all())
        session['search'] = search_word
        session['result'] = [{'name': resource.name, 'description': resource.description} for resource in query_result]
        return render_template('search.html')
    return render_template("index.html", form=form)


@app.route('/search', methods=['get', 'post'])
def search():
    return render_template("search.html")



@app.route('/')
def review():
    pass

if __name__ == "__main__":
    app.run(debug=True, port=5001)
