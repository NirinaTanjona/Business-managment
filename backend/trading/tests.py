from decimal import *
from django.contrib.auth.models import User
from trading.models import Trade, Summary
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status


class SummaryTestCase(APITestCase):
    """
    Test suite for Summaries
    """
    def setUp(self):

        # create 2 authenticated users
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='this_is_a_test',
            email='testuser1@test.com'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='this_is_a_test',
            email='testuser2@test.com'
        )

        Trade.objects.create(user=self.user1, market= "CADJPY", closed_position=-1.01, entry_price=99.562, stop_loss_price=99.272, take_profit_price=100.166,  risk_reward='a' )
        Trade.objects.create(user=self.user1, market= "EURUSD", closed_position=3.96, entry_price=1.05911, stop_loss_price=1.05953, take_profit_price=1.06463,  risk_reward='a' )
        Trade.objects.create(user=self.user1, market= "EURGBP", closed_position=-4.11, entry_price=0.87641, stop_loss_price=0.8784, take_profit_price=0.87212,  risk_reward='a' )
        Trade.objects.create(user=self.user1, market= "EURCHF", closed_position=4.11, entry_price=0.98424, stop_loss_price=0.9848, take_profit_price=0.98805,  risk_reward='a' )
        Trade.objects.create(user=self.user2, market= "AUDUSD", closed_position=-1.07, entry_price=0.67894, stop_loss_price=0.68001, take_profit_price=0.67627,  risk_reward='a' )
        Trade.objects.create(user=self.user2, market= "GBPAUD", closed_position=5.60, entry_price=1.76311, stop_loss_price=1.76262, take_profit_price=1.75488,  risk_reward='a' )

        self.trades = Trade.objects.all()
        self.trades_user1 = Trade.objects.filter(user=self.user1).all()
        self.trades_user2 = Trade.objects.filter(user=self.user2).all()

        #Stats of the 2 users
        self.summary1 = Summary.objects.get(user=self.user1)
        self.summary2 = Summary.objects.get(user=self.user2)

        #The app uses token authentication, each user have 1 unique Token
        self.token1 = Token.objects.get(user = self.user1)
        self.token2 = Token.objects.get(user = self.user2)
        self.client = APIClient()

        #We pass the token in all calls to the API
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)


    def test_get_all_trades(self):
        '''
        test all trade avalaible in the database
        '''
        self.assertEqual(self.trades.count(), 6)

    def test_get_all_trades_by_user(self):
        '''
        test all trade avalaible for each user
        '''
        self.assertEqual(self.trades_user1.count(), 4)
        self.assertEqual(self.trades_user2.count(), 2)

    def test_compare_data_in_summary_with_real_data(self):
        '''
        Compare if values in summary match with the values of trades result
        '''
        self.assertEqual(self.trades_user1.count(), self.summary1.total_number_of_trades)
        self.assertEqual(self.trades_user2.count(), self.summary2.total_number_of_trades)

    def test_total_number_of_winning_trades_value(self):
        '''
        Compare total_numner_of_winning_trade from summary with known data
        summary1 for user1 and summary2 for user2
        '''
        self.assertEqual(self.summary1.total_number_of_winning_trades, 2)
        self.assertEqual(self.summary2.total_number_of_winning_trades, 1)

    def test_largest_winning_trade_for_summary1_and_summary2(self):
        '''
        we query closed_position from Trade wich is a Decimal object so we need to make the
        value for testing in Decimal object
        '''
        self.assertEqual(self.summary1.largest_winning_trade, Decimal(str(4.11)))
        self.assertEqual(self.summary2.largest_winning_trade, Decimal(str(5.60)))

    def test_largest_losing_trade_for_summary1_and_summary2(self):
        '''
        we query closed_position from Trade wich is a Decimal object so we need to make the
        value for testing in Decimal object
        '''
        self.assertEqual(self.summary1.largest_losing_trade, Decimal(str(-4.11)))
        self.assertEqual(self.summary2.largest_losing_trade, Decimal(str(-1.07)))

    def test_win_rate(self):
        '''
        test the winrate output that is like "50%" for exemple
        '''
        win_rate1 = int((2 / 4) * 100)
        win_rate2 = int((1 / 2) * 100)
        self.assertEqual(self.summary1.trade_win_rate, f"{str(win_rate1)}%")
        self.assertEqual(self.summary2.trade_win_rate, f"{str(win_rate2)}%")

    def test_avg_winning_trade(self):
        '''
        test average winning trade
        '''
        avg1 = round(sum([Decimal('3.96'), Decimal('4.11')]) / Decimal('2'), 2)
        avg2 = Decimal('5.60')
        self.assertEqual(self.summary1.avg_winning_trade, Decimal(str(avg1)))
        self.assertEqual(self.summary2.avg_winning_trade, Decimal(str(avg2)))


    # def test_get_one_item(self):
    #     '''
    #     test ItemsViewSet retrieve method
    #     '''
    #     for item in self.items:
    #         response = self.client.get(f'/item/{item.id}/')
    #         self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_order_is_more_than_stock(self):
    #     '''
    #     test Item.check_stock when order.quantity > item.stock
    #     '''
    #     for i in self.items:
    #         current_stock = i.stock
    #         self.assertEqual(i.check_stock(current_stock + 1), False)

    # def test_order_equals_stock(self):
    #     '''
    #     test Item.check_stock when order.quantity == item.stock
    #     '''
    #     for i in self.items:
    #         current_stock = i.stock
    #         self.assertEqual(i.check_stock(current_stock), True)

    # def test_order_is_less_than_stock(self):
    #     '''
    #     test Item.check_stock when order.quantity < item.stock
    #     '''
    #     for i in self.items:
    #         current_stock = i.stock
    #         self.assertTrue(i.check_stock(current_stock - 1), True)

    # def test_create_order_with_more_than_stock(self):
    #     '''
    #     test OrdersViewSet create method when order.quantity > item.stock
    #     '''
    #     for i in self.items:
    #         stock = i.stock
    #         data = {"item": str(i.id), "quantity": str(stock+1)}
    #         response = self.client.post(f'/order/', data)
    #         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_create_order_with_less_than_stock(self):
    #     '''
    #     test OrdersViewSet create method when order.quantity < item.stock
    #     '''
    #     for i in self.items:
    #         data = {"item": str(i.id), "quantity": 1}
    #         response = self.client.post(f'/order/',data)
    #         self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_create_order_with_equal_stock(self):
    #     '''
    #     test OrdersViewSet create method when order.quantity == item.stock
    #     '''
    #     for i in self.items:
    #         stock = i.stock
    #         data = {"item": str(i.id), "quantity": str(stock)}
    #         response = self.client.post(f'/order/',data)
    #         self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_get_all_orders(self):
    #     '''
    #     test OrdersViewSet list method
    #     '''
    #     self.assertEqual(Order.objects.count(), 2)
    #     response = self.client.get('/order/')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)


    # def test_get_one_order(self):
    #     '''
    #     test OrdersViewSet retrieve method
    #     '''
    #     orders = Order.objects.filter(user = self.user)
    #     for o in orders:
    #         response = self.client.get(f'/order/{o.id}/')
    #         self.assertEqual(response.status_code, status.HTTP_200_OK)