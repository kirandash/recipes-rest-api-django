# to create sleep delay
import time

# connections module to check if db connection is available
from django.db import connections
# error that django will throw when db is not available
from django.db.utils import OperationalError
# BaseCommand: class on which we will create our custom command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until DB is available"""

    # handle fn: the fn that runs whenever this command is run
    def handle(self, *args, **options):
        # message on screen for user
        self.stdout.write('Waiting for Database...')
        db_conn = None
        # till db is not connected
        while not db_conn:
            try:
                # try setting up db connection
                db_conn = connections['default']
            except OperationalError:
                # if no connection, throw an error and wait for 1 second
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        # once connection is established, show success msg in green
        self.stdout.write(self.style.SUCCESS('Database available!'))
