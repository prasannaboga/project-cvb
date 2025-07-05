from mongoengine import Document, StringField, DateTimeField, DateField


class Attendance(Document):
  employee_id = StringField(required=True)
  day = DateField(required=True)
  check_in = DateTimeField()
  check_out = DateTimeField()
  status = StringField(
      choices=["present", "absent", "leave", "holiday", "weekend"])

  meta = {
      "collection": "attendances", "strict": True,
      "indexes": [
          {"fields": ["employee_id", "day"], "unique": True},
          {"fields": ["employee_id"]},
          {"fields": ["day"]}
      ]}
