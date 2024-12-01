from mongoengine import Document, StringField, DateTimeField


class Attendance(Document):
  employee_id = StringField(required=True)
  check_in = DateTimeField(required=True)
  check_out = DateTimeField()

  meta = {"collection": "attendances", "strict": True}
