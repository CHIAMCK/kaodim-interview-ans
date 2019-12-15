# Plato I:

1.

https://dbdiagram.io/d/5df4422bedf08a25543f1299

2.

To get the personal board:
```
SELECT b.title
FROM BoardsMembership bm
INNER JOIN Boards b ON bm.board_id = b.id
INNER JOIN Accounts a ON bm.user_id = a.id
WHERE a.id = user_account_id;
```

To get the organization board:
```
SELECT b.title
FROM BoardsMembership bm
INNER JOIN Boards bm ON bm.board_id = b.id
INNER JOIN Organizations org ON bm.organization_id = org.id
WHERE org.id = user_organization_id;
```

For each boards, run the following sql statement to get the latest 5 cards:
```
SELECT c.title
FROM Cards c
INNER JOIN Boards b ON c.board_id = b.id
WHERE b.id = board_id
ORDER BY c.created_at DESC
LIMIT 5;
```

For each cards, run the following sql statement to get the completed/ total tasks:
```
SELECT COUNT(t.id) AS [Completed Tasks]
FROM Cards c
INNER JOIN TaskList tl on c.id=tl.cards_id
INNER JOIN Tasks t on tl.id = t.task_list_id
GROUP BY state
HAVING state = ‘Completed’
```

**How would you improve the sql query?**

Add index to the state column (Completed …) of Tasks table. This can prevent table scans with time cost O(n) which slow down the performance when the data size is huge.

ORDER BY query can be improved if we add index on the created_at column. By doing so, ORDER BY with LIMIT query can be executed without scanning and sorting full result set.

To avoid N+1 query, we can use select_related(), prefetch_related() provided by django ORM to select additional related-object data when it executes its query. By doing so, we can reduce query count. Every query spends a certain amount of time traveling to and from the database server

querying only the required data


3.

A list of Plato's dependencies:

framework - Django
database – Postgresql
server – AWS ec2 instance
web server – nginx
app server - Gunicorn

3rd party packages:
- django-allauth, to handle user authentication and Facebook OAuth , https://django-allauth.readthedocs.io/en/latest/installation.html


4.

A list of application design patterns and assumptions:

Design patterns:

use normalization to organize data into multiple related tables to minimize data redundancy.


Assumption:

Every person who uses Plato has their own user account.

Account is used as a representation of user.

User can create an organization. The creator of organization would be the owner of the board. Members can be added to the organization.

Members of a organization can see all the boards belong to the organization

Each account, organization can only subscribe to one of the plans

A board can be owned by individual or a organization.

Each card can only have one task list.

Each card can only be assigned to one user.


# Plato II:
```
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
```

```
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
```

# Plato III

1.

https://dbdiagram.io/d/5df4422bedf08a25543f1299


2.
```
calculate monthly fee
if it is individual user:
	monthly_fee = 3*number_of_board
else if startup plan:
	monthly_fee = 20 + additional_user*7
else if business plan:
	monthly_fee = 35 +  additional_user*6
else if enterprise plan:
	monthly_fee = 60 + additional_user*4
return monthly_fee

calculate annual fee
if it is individual user:
	annual_fee = 3*number_of_board*12
else if startup plan:
	annual_fee = (18 + additional_user*7)*12
else if business plan:
	annual_fee = (32 +  additional_user*6)*12
else if enterprise plan:
	annual_fee = (55 + additional_user*4)*12
return annual_fee
```

3.

Make changes to model and migrate the table to database.

Add new subscription plan (business) calculation to it. Change the pricing.

Need to add logic to check whether the user subscribe to any plan during the acquisition campaigns.
