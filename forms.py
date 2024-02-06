from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    search = StringField("word", validators=[DataRequired()],
                         render_kw={"placeholder": "Search for resources", "class": "form-control text-bg-dark mr-3"})
    submit = SubmitField("Search", render_kw={"class": "btn btn-warning"})


class CreateResourceForm(FlaskForm):
    name = StringField("Blog Post Title", validators=[DataRequired()])
    description = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


class ReviewForm(FlaskForm):
    rating = SelectField('Rate the resource', choices=[(1, '⭐'), (2, '⭐⭐'),(3, '⭐⭐⭐'),(4, '⭐⭐⭐⭐'),(5, '⭐⭐⭐⭐⭐')])
    review_text = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")
