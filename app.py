from flask import Flask, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_migrate import Migrate
from forms import SearchForm, CreateResourceForm, ReviewForm
from flask_bootstrap import Bootstrap4
from flask_ckeditor import CKEditor

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBfqeuibnvuiguosdk139r93b'


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resources.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)
bootstrap = Bootstrap4(app)
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
        session['search'] = form.search.data
        return redirect(url_for('search'))
    return render_template("index.html", form=form)


@app.route('/search', methods=['get', 'post'])
def search():
    search_word = session.get('search')
    form = SearchForm(search=search_word)
    query_result = set(Resources.query.filter(Resources.name.like(f'%{search_word}%')).all())
    query_result.update(Resources.query.filter(Reviews.content.like(f'%{search_word}%')).all())
    if form.validate_on_submit():
        search_word = form.search.data
        query_result = set(Resources.query.filter(Resources.name.like(f'%{search_word}%')).all())
        query_result.update(Resources.query.filter(Reviews.content.like(f'%{search_word}%')).all())
        return render_template("search.html", form=form, resources=query_result)
    return render_template("search.html", form=form, resources=query_result)


@app.route('/comment/<int:resource_id>', methods=['get', 'post'])
def review(resource_id):
    form = ReviewForm()
    resource = db.get_or_404(Resources,resource_id)
    if form.validate_on_submit():
        new_review = Reviews(
            rating=form.rating.data,
            content=form.review_text.data,
            resource_id=resource_id
        )
        db.session.add(new_review)
        print("review added successfully!")
        return redirect(url_for('search'))
    return render_template('add_review.html', form=form, resource=resource)


@app.route('/about', methods=['get'])
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True, port=5001)
