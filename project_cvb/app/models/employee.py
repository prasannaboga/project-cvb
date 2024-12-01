from mongoengine import Document, StringField, DateField


class Employee(Document):
  name = StringField(required=True, max_length=255)
  date_of_birth = DateField(required=False)

  meta = {"collection": "employees", "strict": True}
