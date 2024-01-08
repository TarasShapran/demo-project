import time

from django.core.management import BaseCommand
from django.db import OperationalError, connection
from django.db.backends.mysql.base import DatabaseWrapper

# from django.db.backends.postgresql.base import DatabaseWrapper for postgres

connection: DatabaseWrapper = connection


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Wait for DB...')
        db_con = False

        while not db_con:
            try:
                connection.ensure_connection()
                db_con = True
            except OperationalError:
                self.stdout.write('Database unavailable, wait 3 second...')
                time.sleep(3)

        self.stdout.write('Database is available!!!')
