from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo, ValidationError

class NiceClassificationForm(FlaskForm):
    cnaes=StringField('CNAEs',validators=[DataRequired(),Length(min=2,max=50)])
    products=StringField('Lista de produtos',validators=[Length(min=2,max=50)])
    products=StringField('Lista de produtos',validators=[Length(min=2,max=50)])
    submit=SubmitField(' Ver classificações de Nice sugeridas.')
    # def validate_cnaes(self,cnaes):
    #     if cnaes:
    #         raise ValidationError('That username is taken, please choose another one')