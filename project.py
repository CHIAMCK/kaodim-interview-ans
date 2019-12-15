
class Organization:
    def __init__(self, name, number_of_users, plan, number_of_boards):
        self.name = name
        self.number_of_users = number_of_users
        self.subscribe_plan = plan
        self.number_of_boards = number_of_boards

    def add_member(self, number_of_users):
        self.number_of_users+=number_of_users

# function to calculate the monthly subscription fee
def monthly_subscription_payable_amount(org=None):
    amount = 0
    if org is None:
        amount = 1*2
    elif org.subscribe_plan == 'startup':
        amount = calculate_amount(org, 20, 5, 7, 'monthly')
    elif org.subscribe_plan == 'enterprise':
        amount = calculate_amount(org, 60, 20, 6, 'monthly')
    return amount

# function to calculate the annual subscription fee
def annually_subscription_payable_amount(org=None):
    amount = 0
    additional_cost = 0
    if org is None:
        amount = 1*2*12
    elif org.subscribe_plan == 'startup':
        amount = calculate_amount(org, 18, 5, 7, 'annually')
    elif org.subscribe_plan == 'enterprise':
        amount = calculate_amount(org, 55, 20, 6, 'annually')
    return amount

# function to calculate the subscription fee
def calculate_amount(org, fee_per_month, max_members, additional_fee, type):
    additional_cost = 0
    number_of_users = org.number_of_users
    months = 1
    if type == 'annually':
        months = 12
    if number_of_users > max_members:
        additional_cost = (number_of_users - max_members)*additional_fee*months
    amount = fee_per_month*months + additional_cost
    return amount


# test cases
import unittest

class PricingTestCase(unittest.TestCase):
    def setUp(self):
        self.startup = Organization('kaodim', 2, 'startup', 4)
        self.enterprise = Organization('kaodim', 20, 'enterprise', 4)

    # test monthly fee for startup plan with 2 users
    def test_startup_monthly_fee(self):
        # execution
        amount = monthly_subscription_payable_amount(self.startup)

        # assertion
        self.assertEqual(amount, 20)

    # test annual fee for startup plan with 2 users
    def test_startup_monthly_fee(self):
        # execution
        amount = annually_subscription_payable_amount(self.startup)

        # assertion
        self.assertEqual(amount, 216)

    # test monthly fee for startup plan with 6 users
    def test_startup_monthly_fee_with_six_users(self):
        # setup
        self.startup.add_member(4)

        # execution
        amount = monthly_subscription_payable_amount(self.startup)

        # assertion
        self.assertEqual(amount, 27)

    # test annual fee for startup plan with 6 users
    def test_startup_annual_fee_with_six_users(self):
        # setup
        self.startup.add_member(4)

        # execution
        amount = annually_subscription_payable_amount(self.startup)

        # assertion
        self.assertEqual(amount, 300)

    # test monthly fee for solo plan
    def test_solo_monthly_fee(self):
        # execution
        amount = monthly_subscription_payable_amount()

        # assertion
        self.assertEqual(amount, 2)

    # test annual fee for solo plan
    def test_solo_annual_fee(self):
        # execution
        amount = annually_subscription_payable_amount()

        # assertion
        self.assertEqual(amount, 24)

    # test monthly fee for enterprise plan with number of users equal or less than 50
    def test_enterprise_monthly_fee_with_fifty_users(self):
        # execution
        amount = monthly_subscription_payable_amount(self.enterprise)

        # assertion
        self.assertEqual(amount, 60)

    # test annual fee for enterprise plan
    def test_enterprise_annual_fee_with_fifty_users(self):
        # execution
        amount = annually_subscription_payable_amount(self.enterprise)

        # assertion
        self.assertEqual(amount, 660)

    # test monthly fee for enterprise plan with number of users more than 50
    def test_enterprise_monthly_fee_with_thirty_users(self):
        # startup
        self.enterprise.add_member(10)
        # execution
        amount = monthly_subscription_payable_amount(self.enterprise)

        # assertion
        self.assertEqual(amount, 120)

    # test annual fee for enterprise plan with number of users more than 50
    def test_enterprise_annual_fee_with_thirty_users(self):
        # startup
        self.enterprise.add_member(10)

        # execution
        amount = annually_subscription_payable_amount(self.enterprise)

        # assertion
        self.assertEqual(amount, 1380)
