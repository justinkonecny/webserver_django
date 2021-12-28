import time

from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = "Wait for the database connection to be ready."

    def add_arguments(self, parser) -> None:
        super().add_arguments(parser)
        parser.add_argument(
            "-t",
            "--timeout",
            dest="timeout",
            type=int,
            default=1,
            help="Timeout (in seconds)",
        )

    def handle(self, *args, **options) -> None:
        while True:
            try:
                connection.connect()
            except OperationalError:
                self.stdout.write("Error connecting to the Database. Waiting...")
                time.sleep(options["timeout"])
            else:
                self.stdout.write("Database is ready for connections.")
                break
