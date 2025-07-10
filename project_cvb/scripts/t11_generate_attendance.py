import argparse
import logging
import random
import sys
from datetime import datetime, timedelta

from project_cvb.app.models.attendance import Attendance
from project_cvb.config.mongodb_config import initialize_mongodb

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


def run():
  initialize_mongodb()
  parser = argparse.ArgumentParser(
      description="Generate attendance records for past N days.")
  parser.add_argument("--past_days", type=int, default=30,
                      help="Number of past days to generate attendance for.")
  parser.add_argument("--delete", type=bool, default=False,
                      help="Delete existing attendance records")
  parser.add_argument("--fillrecords", type=bool, default=True,
                      help="Delete existing attendance records")
  args = parser.parse_args(sys.argv[1:])
  logger.info(f"agrguments: {vars(args)}")
  if args.delete:
    logger.info("Deleting existing attendance records...")
    Attendance.objects.delete()
    logger.info("Deleted existing attendance records.")
  else:
    generate_attendance(args)


def generate_attendance(args):
  today = datetime.now()
  if getattr(args, "fillrecords", True):
    last_attendance = Attendance.objects().order_by("-day").first()
    if last_attendance:
      start_date = datetime.combine(last_attendance.day, datetime.min.time()) + timedelta(days=1)
    else:
      start_date = today - timedelta(days=args.past_days)
  else:
    start_date = today - timedelta(days=args.past_days)
  end_date = today

  logger.info(
      f"generating attendance for past {args.past_days} days. duration: {start_date} to {end_date}")
  for i in range(1, 16):
    employee_id = f"emp_{i:02d}"
    logger.info(f"attendance for employee: {employee_id}")
    for single_date in (start_date + timedelta(n) for n in range((end_date - start_date).days + 1)):
      logger.info(f" processing date: {single_date.date()}")
      weekday = single_date.weekday()  # 5 = Saturday, 6 = Sunday
      if weekday in (5, 6):  # Saturday or Sunday
        random_value = random.random()
        if random_value <= 0.09:
          logger.info(
              f"  weekend present status for random value: {random_value}")
          check_in_time = random_time(single_date, punch_type="check_in")
          check_out_time = random_time(single_date, punch_type="check_out")
          status = "present"
        else:
          check_in_time = None
          check_out_time = None
          status = "weekend"
      else:
        random_value = random.random()
        if random_value < 0.10:
          status = "leave"
          check_in_time = None
          check_out_time = None
        elif random_value < 0.12:
          status = "absent"
          check_in_time = None
          check_out_time = None
        else:
          check_in_time = random_time(single_date, punch_type="check_in")
          check_out_time = random_time(single_date, punch_type="check_out")
          status = "present"

      update_fields = {"set__status": status,
                       "set__check_in": check_in_time, "set__check_out": check_out_time}

      check_in_time = random_time(single_date, punch_type="check_in")
      check_out_time = random_time(single_date, punch_type="check_out")
      attendance = Attendance.objects(
          employee_id=employee_id, day=single_date.date())
      attendance = attendance.modify(upsert=True, new=True, **update_fields)
      logger.info(f"  saved attendance record: {attendance.to_json()}")


def random_time(date, punch_type="check_in"):
  """Generate a random time for the given date."""
  if punch_type == "check_in":
    # 10% chance for early (<8) or late (>10) check-in
    if random.random() < 0.2:
      if random.choice([True, False]):
        hour = random.randint(6, 7)  # Early: 6-7 AM
      else:
        hour = random.randint(11, 13)  # Late: 11 AM - 1 PM
    else:
      hour = random.randint(8, 10)  # Normal: 8-10 AM
  else:  # check_out
    # 10% chance for early (<17) or late (>19) check-out
    if random.random() < 0.2:
      if random.choice([True, False]):
        hour = random.randint(15, 16)  # Early: 3-4 PM
      else:
        hour = random.randint(20, 22)  # Late: 8-10 PM
    else:
      hour = random.randint(17, 19)  # Normal: 5-7 PM
  minute = random.randint(0, 59)
  second = random.randint(0, 59)
  return datetime.combine(date, datetime.min.time()).replace(hour=hour, minute=minute, second=second)


if __name__ == "__main__":
  run()
