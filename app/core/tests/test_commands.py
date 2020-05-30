# mock library
from unittest.mock import patch

# to call a command
from django.core.management import call_command
# operational error that Django throws when there is no DB
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # overwrite the default functionality of getitem fn
            # to always return true
            gi.return_value = True
            # wait_for_db : management command we will create
            call_command('wait_for_db')
            # check if get_item is called once
            self.assertEqual(gi.call_count, 1)

    # Functionality - db calls should keep trying until success
    # will mock by failing for 5 times and then returning true
    # patch decorator with time.sleep to not wait for subsequent calls to db
    # to improve test speed by setting time.sleep to return True and no delay
    # in real code, we will have some delay (1s) in getitem b/w db calls
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # add side effect to raise operational error for 5 times
            # and return True for 6th time
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            # check if get_item is called six times
            self.assertEqual(gi.call_count, 6)
