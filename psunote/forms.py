

from wtforms import Field, widgets, StringField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

# class TagListField(Field):
#     widget = widgets.TextInput()

#     def __init__(self, label="", validators=None, remove_duplicates=True, **kwargs):
#         super().__init__(label, validators, **kwargs)
#         self.remove_duplicates = remove_duplicates
#         self.data = []

#     def process_formdata(self, valuelist):
#         data = []
#         if valuelist:
#             data = [x.strip() for x in valuelist[0].split(",")]

#         if not self.remove_duplicates:
#             self.data = data
#             return

#         self.data = []
#         for d in data:
#             if d not in self.data:
#                 self.data.append(d)

#     def _value(self):
#         if isinstance(self.data, list):
#             return ", ".join(str(tag) for tag in self.data)  # Convert list to comma-separated string
#         return self.data or ""


# class NoteForm(FlaskForm):
#     title = StringField('Title', validators=[DataRequired()])
#     description = TextAreaField('Description', validators=[DataRequired()])
#     tags = TagListField('Tags') 

class TagListField(Field):
    widget = widgets.TextInput()

    def __init__(self, label="", validators=None, remove_duplicates=True, **kwargs):
        super().__init__(label, validators, **kwargs)
        self.remove_duplicates = remove_duplicates
        self.data = []

    def process_formdata(self, valuelist):
        if valuelist:
            data = [x.strip() for x in valuelist[0].split(",")]
            if self.remove_duplicates:
                self.data = list(dict.fromkeys(data))
            else:
                self.data = data

    def _value(self):
        if isinstance(self.data, list):
            return ", ".join(str(tag) for tag in self.data)
        return self.data or ""


class NoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    tags = TagListField('Tags')  # ฟิลด์สำหรับแท็ก
