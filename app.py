from flask import Flask
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text

app = Flask(__name__)


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resources.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


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
    return render_template("index.html")

@app.route('/', methods=['get', 'post'])
def get_search_results():
    pass

