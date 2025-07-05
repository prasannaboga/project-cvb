import argparse
import sys
from datetime import datetime, timedelta

from project_cvb.app.models.attendance import Attendance
from project_cvb.config.mongodb_config import initialize_mongodb


def run():
    parser = argparse.ArgumentParser(
        description="Generate attendance records for past N days."
    )
    parser.add_argument(
        "--past_days", type=int, default=30,
        help="Number of past days to generate attendance for."
    )
    args = parser.parse_args(sys.argv[1:])
    print(vars(args))
    generate_attendance(args)

def generate_attendance(args):
    # Your business logic
    print(f"Generating attendance for past {args.past_days} days")


if __name__ == "__main__":
  parser = argparse.ArgumentParser(
      description="Generate attendance records for past N days.")
  parser.add_argument("--past_days", type=int, default=30,
                      help="Number of past days to generate attendance for.")
  args = parser.parse_args()
  print(f"Generating attendance for past {args.past_days} days")
  run(args)
