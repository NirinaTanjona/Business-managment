from decimal import *
from django.contrib.auth.models import User
from django.db.models import Max, Min, Avg, Sum
from trading.models import Trade, Summary
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status
import json


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
        self.user1.summary.update_balance(300)
        self.user2.summary.update_balance(500)
        self.user1.summary.set_starting_balance(300)
        self.user2.summary.set_starting_balance(500)
        self.starting_balance1 = self.user1.summary.starting_balance
        self.starting_balance2 = self.user2.summary.starting_balance


        Trade.objects.create(user=self.user1, summary=self.user1.summary, market= "CADJPY", closed_position=-1.01, entry_price=99.562, stop_loss_price=99.272, actual_exit_price=100.166)
        Trade.objects.create(user=self.user1, summary=self.user1.summary, market= "EURUSD", closed_position=2.76, entry_price=1.05911, stop_loss_price=1.05953, actual_exit_price=1.06463)
        Trade.objects.create(user=self.user1, summary=self.user1.summary, market= "EURGBP", closed_position=-5.1, entry_price=0.87641, stop_loss_price=0.8784, actual_exit_price=0.87212)
        Trade.objects.create(user=self.user1, summary=self.user1.summary, market= "EURCHF", closed_position=8.11, entry_price=0.98424, stop_loss_price=0.9848, actual_exit_price=0.98805)
        Trade.objects.create(user=self.user2, summary=self.user2.summary, market= "AUDUSD", closed_position=-1.06, entry_price=0.67894, stop_loss_price=0.68001, actual_exit_price=0.67627)
        Trade.objects.create(user=self.user2, summary=self.user2.summary, market= "GBPAUD", closed_position=4.6, entry_price=1.76311, stop_loss_price=1.76262, actual_exit_price=1.75488)
        Trade.objects.create(user=self.user2, summary=self.user2.summary, market= "AUDCAD", closed_position=-1.89, entry_price=0.92445, stop_loss_price=0.92636, actual_exit_price=0.91954)
        Trade.objects.create(user=self.user2, summary=self.user2.summary, market= "USDCAD", closed_position=0.53, entry_price=1.36056, stop_loss_price=1.36094, actual_exit_price=1.36381)
        Trade.objects.create(user=self.user2, summary=self.user2.summary, market= "XAUUSD", closed_position=-2.80, entry_price=1911.64, stop_loss_price=1914.43, actual_exit_price=1930.32)

        self.trades = Trade.objects.all()
        self.trades_user1 = Trade.objects.filter(user=self.user1).all()
        self.trades_user2 = Trade.objects.filter(user=self.user2).all()

        #Stats of the 2 users
        self.summary1 = Summary.objects.get(user=self.user1)
        self.summary2 = Summary.objects.get(user=self.user2)

        self.balance1 = self.user1.summary.balance
        self.balance2 = self.user2.summary.balance


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
        self.assertEqual(self.trades.count(), 9)


    def test_get_all_trades_by_user(self):
        '''
        test all trade avalaible for each user
        '''
        self.assertEqual(self.trades_user1.count(), 4)
        self.assertEqual(self.trades_user2.count(), 5)
        response = self.client.get('/trade/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_summary(self):
        '''
        test Summary retrieve method
        '''
        response = self.client.get('/summary/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_compare_data_in_summary_with_real_data(self):
        '''
        Compare if values in summary match with the values of trades result
        '''
        self.assertEqual(self.trades_user1.count(), self.summary1.total_number_of_trades)
        self.assertEqual(self.trades_user2.count(), self.summary2.total_number_of_trades)

    def test_total_number_of_winning_trades_value(self):
        '''
        Compare total_number_of_winning_trade from summary with known data
        summary1 for user1 and summary2 for user2
        '''
        count_winning_trade_user1 = 0
        count_winning_trade_user2 = 0
        for trade in self.trades_user1:
            if trade.closed_position > 0:
                count_winning_trade_user1 += 1
        for trade in self.trades_user2:
            if trade.closed_position > 0:
                count_winning_trade_user2 += 1
        self.assertEqual(self.summary1.total_number_of_winning_trades, count_winning_trade_user1)
        self.assertEqual(self.summary2.total_number_of_winning_trades, count_winning_trade_user2)

    def test_total_number_of_losing_trades_value(self):
        '''
        Compare total_numner_of_losing_trade from summary with known data
        summary1 for user1 and summary2 for user2
        '''
        count_losing_trade_user1 = 0
        count_losing_trade_user2 = 0
        for trade in self.trades_user1:
            if trade.closed_position > 0:
                count_losing_trade_user1 += 1
        for trade in self.trades_user2:
            if trade.closed_position < 0:
                count_losing_trade_user2 += 1
        self.assertEqual(self.summary1.total_number_of_losing_trades, count_losing_trade_user1)
        self.assertEqual(self.summary2.total_number_of_losing_trades, count_losing_trade_user2)

    def test_largest_winning_trade_for_summary1_and_summary2(self):
        '''
        we query closed_position from Trade wich is a Decimal object so we need to make the
        value for testing in Decimal object
        '''
        largest_winning_trade_user1 = self.trades_user1.aggregate(Max('closed_position'))['closed_position__max']
        largest_winning_trade_user2 = self.trades_user2.aggregate(Max('closed_position'))['closed_position__max']
        self.assertEqual(self.summary1.largest_winning_trade, largest_winning_trade_user1)
        self.assertEqual(self.summary2.largest_winning_trade, largest_winning_trade_user2)

    def test_largest_losing_trade_for_summary1_and_summary2(self):
        '''
        we query closed_position from Trade wich is a Decimal object so we need to make the
        value for testing in Decimal object
        '''
        largest_losing_trade_user1 = self.trades_user1.aggregate(Min('closed_position'))['closed_position__min']
        largest_losing_trade_user2 = self.trades_user2.aggregate(Min('closed_position'))['closed_position__min']
        self.assertEqual(self.summary1.largest_losing_trade, largest_losing_trade_user1)
        self.assertEqual(self.summary2.largest_losing_trade, largest_losing_trade_user2)

    def test_win_rate(self):
        '''
        test the winrate output that is like "50%" for exemple
        '''
        win_rate1 = (self.trades_user1.filter(closed_position__gt=0).count() / self.trades_user1.count()) * 100
        win_rate2 = (self.trades_user2.filter(closed_position__gt=0).count() / self.trades_user2.count()) * 100
        self.assertEqual(self.summary1.trade_win_rate, f"{str(int(win_rate1))}%")
        self.assertEqual(self.summary2.trade_win_rate, f"{str(int(win_rate2))}%")

    def test_avg_winning_trade(self):
        '''
        test average winning trade
        '''
        avg1 = self.trades_user1.filter(closed_position__gt=0).aggregate(Avg('closed_position'))['closed_position__avg']
        avg2 = self.trades_user2.filter(closed_position__gt=0).aggregate(Avg('closed_position'))['closed_position__avg']
        self.assertEqual(self.summary1.avg_winning_trade, avg1.quantize(Decimal('0.00'), rounding='ROUND_HALF_UP'))
        self.assertEqual(self.summary2.avg_winning_trade, avg2.quantize(Decimal('0.00'), rounding='ROUND_HALF_UP'))

    def test_avg_losing_trade(self):
        '''
        test average losing trade
        '''
        avg1 = self.trades_user1.filter(closed_position__lt=0).aggregate(Avg('closed_position'))['closed_position__avg']
        avg2 = self.trades_user2.filter(closed_position__lt=0).aggregate(Avg('closed_position'))['closed_position__avg']
        self.assertEqual(self.summary1.avg_losing_trade, avg1.quantize(Decimal('0.00'), rounding='ROUND_HALF_UP'))
        self.assertEqual(self.summary2.avg_losing_trade, avg2.quantize(Decimal('0.00'), rounding='ROUND_HALF_UP'))

    def test_update_balance(self):
        '''
        test balance in each instance of trade
        '''
        sum1 = self.trades_user1.aggregate(Sum('closed_position'))['closed_position__sum']
        sum2 = self.trades_user2.aggregate(Sum('closed_position'))['closed_position__sum']
        self.assertEqual(self.summary1.balance, (self.starting_balance1 + sum1).quantize(Decimal('0.00'), rounding='ROUND_HALF_UP'))
        self.assertEqual(self.summary2.balance, (self.starting_balance2 + sum2).quantize(Decimal('0.00'), rounding='ROUND_HALF_UP'))

    def test_update_total_profit_loss(self):
        '''
        test total_profit_loss in each instance of trade
        '''
        sum1 = self.trades_user1.aggregate(Sum('closed_position'))['closed_position__sum']
        sum2 = self.trades_user2.aggregate(Sum('closed_position'))['closed_position__sum']
        self.assertEqual(self.summary1.total_profit_loss, sum1.quantize(Decimal('0.00'), rounding='ROUND_HALF_UP'))
        self.assertEqual(self.summary2.total_profit_loss, sum2.quantize(Decimal('0.00'), rounding='ROUND_HALF_UP'))

    def test_average_profit_loss_per_trade(self):
        '''
        test average profit loss per trade
        '''
        num1 = self.trades_user1.count()
        num2 = self.trades_user2.count()
        sum1 = self.trades_user1.aggregate(Sum('closed_position'))['closed_position__sum']
        sum2 = self.trades_user2.aggregate(Sum('closed_position'))['closed_position__sum']
        val1 = sum1 / num1
        val2 = sum2 / num2
        self.assertEqual(self.summary1.average_profit_loss_per_trade, val1.quantize(Decimal('0.00'), rounding='ROUND_HALF_UP'))
        self.assertEqual(self.summary2.average_profit_loss_per_trade, val2.quantize(Decimal('0.00'), rounding='ROUND_HALF_UP'))

    def test_return_of_investment(self):
        '''
        test return of investment
        '''
        sum1 = self.trades_user1.aggregate(Sum('closed_position'))['closed_position__sum']
        sum2 = self.trades_user2.aggregate(Sum('closed_position'))['closed_position__sum']
        if sum1:
            val1 = (sum1 / self.starting_balance1) * 100
        else:
            val1 = "0%"
        self.assertEqual(self.summary1.return_of_investment, f"{round(val1, 2)}%")

        if sum2:
            val2 = (sum2/ self.starting_balance2) * 100
        else:
            val2 = "0%"
        self.assertEqual(self.summary2.return_of_investment, f"{round(val2, 2)}%")

    def test_average_risk_per_trade(self):
        '''
        test average risk per trade
        '''

        # (average losing trade / balance) * 100
        avg1 = self.trades_user1.filter(closed_position__lt=0).aggregate(Avg('closed_position'))['closed_position__avg']
        avg2 = self.trades_user2.filter(closed_position__lt=0).aggregate(Avg('closed_position'))['closed_position__avg']
        self.assertEqual(self.summary1.average_risk_per_trade, f"{round((avg1 / self.balance1) * 100, 2)}%")
        self.assertEqual(self.summary2.average_risk_per_trade, f"{round((avg2 / self.balance2) * 100, 2)}%")


    def test_average_reward_per_trade(self):
        '''
        test average reward per trade
        '''

        # (average winning trade / balance) * 100
        avg1 = self.trades_user1.filter(closed_position__gt=0).aggregate(Avg('closed_position'))['closed_position__avg']
        avg2 = self.trades_user2.filter(closed_position__gt=0).aggregate(Avg('closed_position'))['closed_position__avg']
        self.assertEqual(self.summary1.average_reward_per_trade, f"{round((avg1 / self.balance1) * 100, 2)}%")
        self.assertEqual(self.summary2.average_reward_per_trade, f"{round((avg2 / self.balance2) * 100, 2)}%")


    def test_average_risk_reward_per_trade(self):
        '''
        test average risk reward per trade
        '''

        # (average winning trade / average losing trade) * 100
        avg_win_1 = self.trades_user1.filter(closed_position__gt=0).aggregate(Avg('closed_position'))['closed_position__avg']
        avg_ls_1 = self.trades_user1.filter(closed_position__lt=0).aggregate(Avg('closed_position'))['closed_position__avg']
        avg_win_2 = self.trades_user2.filter(closed_position__gt=0).aggregate(Avg('closed_position'))['closed_position__avg']
        avg_ls_2 = self.trades_user2.filter(closed_position__lt=0).aggregate(Avg('closed_position'))['closed_position__avg']
        val1, val2 = 0,0
        if avg_win_1 and avg_ls_1:
            val1 = round(avg_win_1 / abs(avg_ls_1), 2)
        elif avg_win_1 == 0:
            val1 = 0
        elif avg_ls_1 == 0:
            val1 = avg_win_1

        if avg_win_2 and avg_ls_2:
            val2 = round(avg_win_2 / abs(avg_ls_2), 2)
        elif avg_win_2 == 0:
            val2 = 0
        elif avg_ls_2 == 0:
            val = avg_win_2
        self.assertEqual(self.summary1.average_risk_reward, f"1:{val1}")
        self.assertEqual(self.summary2.average_risk_reward, f"1:{val2}")


    def test_update_partial_on_summary(self):
        '''
        test send patch method to summary
        '''
        data = {"starting_balance": 500}
        response = self.client.patch(f'/summary/{self.summary1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_update_partial_on_trade(self):
        '''
        test send patch method to trade
        '''
        data = {"closed_position": 500}
        for trade in self.trades_user1.all():
            response = self.client.patch(f'/trade/{trade.id}/', data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_trade(self):
        '''
        test delete trade
        '''
        for trade in self.trades_user1.all():
            response = self.client.delete(f'/trade/{trade.id}/')
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_create_trade_on_trade(self):
        '''
        test create trade on Trade model
        '''
        data = {"market": "GBPAUD", "closed_position": 4.6, "entry_price": 1.76311, "stop_loss_price": 1.76262, "actual_exit_price": 1.75488 }
        response = self.client.post('/trade/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_use(self):
        '''
        test create new use
        '''
        data = {"username": "tanjona", "email": "tanjona@test.com", "password": "tanjona_password"}
        response = self.client.post('/sign-up/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_trades_on_summary_model(self):
        '''
        test trades on summary models
        '''
        self.assertEqual(self.summary1.trades.all().count(), self.trades_user1.count())
        self.assertEqual(self.summary2.trades.all().count(), self.trades_user2.count())
