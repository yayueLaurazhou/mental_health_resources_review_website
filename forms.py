from flask_wtf import FlaskForm
from WTFforms import StringField, SubmitField
from flask_ckeditor import CKEditorField


# WTForm for creating a blog post
class CreateResourceForm(FlaskForm):
    name = StringField("Blog Post Title", validators=[DataRequired()])
    description = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

# Create a form to add comments
class CommentForm(FlaskForm):
    comment_text = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")

