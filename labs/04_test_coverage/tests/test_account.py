import json
from random import randrange
from unittest import TestCase
from models import db
from models.account import Account, DataValidationError

ACCOUNT_DATA = {}

class TestAccountModel(TestCase):
    """Test Account Model"""

    @classmethod
    def setUpClass(cls):
        """ Load data needed by tests """
        db.create_all()  # make our sqlalchemy tables
        global ACCOUNT_DATA
        with open('tests/fixtures/account_data.json') as json_data:
            ACCOUNT_DATA = json.load(json_data)

    @classmethod
    def tearDownClass(cls):
        """Disconnect from database"""
        db.session.close()

    def setUp(self):
        """Truncate the tables"""
        self.rand = randrange(0, len(ACCOUNT_DATA))
        db.session.query(Account).delete()
        db.session.commit()

    def tearDown(self):
        """Remove the session"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_all_accounts(self):
        """Test creating multiple Accounts"""
        for data in ACCOUNT_DATA:
            account = Account(**data)
            account.create()
        self.assertEqual(len(Account.all()), len(ACCOUNT_DATA))

    def test_create_an_account(self):
        """Test Account creation using known data"""
        data = ACCOUNT_DATA[self.rand]  # get a random account
        account = Account(**data)
        account.create()
        self.assertEqual(len(Account.all()), 1)

    def test_update_account(self):
        """Test updating an Account"""
        data = ACCOUNT_DATA[self.rand]
        account = Account(**data)
        account.create()
        account.name = "Updated Name"
        account.update()
        updated_account = Account.find(account.id)
        self.assertEqual(updated_account.name, "Updated Name")

    def test_update_without_id(self):
        """Test update error when ID is missing"""
        account = Account()
        with self.assertRaises(DataValidationError):
            account.update()

    def test_delete_account(self):
        """Test deleting an Account"""
        data = ACCOUNT_DATA[self.rand]
        account = Account(**data)
        account.create()
        self.assertEqual(len(Account.all()), 1)
        account.delete()
        self.assertEqual(len(Account.all()), 0)

    def test_to_dict(self):
        """Test Account serialization to dict"""
        data = ACCOUNT_DATA[self.rand]
        account = Account(**data)
        result = account.to_dict()
        self.assertEqual(result["name"], data["name"])
        self.assertEqual(result["email"], data["email"])

    def test_from_dict(self):
        """Test Account deserialization from dict"""
        data = ACCOUNT_DATA[self.rand]
        account = Account()
        account.from_dict(data)
        self.assertEqual(account.name, data["name"])
        self.assertEqual(account.email, data["email"])

    def test_all_accounts(self):
        """Test retrieving all accounts"""
        for data in ACCOUNT_DATA:
            account = Account(**data)
            account.create()
        all_accounts = Account.all()
        self.assertEqual(len(all_accounts), len(ACCOUNT_DATA))

    def test_find_account(self):
        """Test finding an Account by ID"""
        data = ACCOUNT_DATA[self.rand]
        account = Account(**data)
        account.create()
        found_account = Account.find(account.id)
        self.assertIsNotNone(found_account)
        self.assertEqual(found_account.name, data["name"])

    def test_find_account_not_found(self):
        """Test finding an Account that doesn't exist"""
        account = Account.find(0)
        self.assertIsNone(account)
