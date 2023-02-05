import math
from django.db import models
from django.contrib.auth.models import User
from utils.model_abstracts import Model
from django_extensions.db.models import (
    TimeStampedModel,
    ActivatorModel,
    TitleSlugDescriptionModel
)

class Summary(
    ActivatorModel ,
    Model):

    """
    trading.Summary
    store all stat of trade of a particular user
    """

    def __str__(self):
        return f"{self.user.username} stats"

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    starting_balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    total_number_of_trades = models.PositiveIntegerField(default=0)
    total_number_of_winning_trades = models.PositiveIntegerField(default=0)
    total_number_of_losing_trades = models.PositiveIntegerField(default=0)
    total_number_of_be_trade = models.PositiveIntegerField(default=0)
    largest_winning_trade = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    largest_losing_trade = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    avg_winning_trade = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    avg_losing_trade = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    total_trade_costs = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    total_profit_loss = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    average_profit_loss_per_trade = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    return_of_investment = models.CharField(default='0%', max_length=10)
    average_risk_per_trade = models.CharField(default='1:1', max_length=10)
    average_risk_reward_per_trade = models.CharField(default='0%', max_length=10)
    trade_win_rate = models.CharField('0%', max_length=10)

    def update_total_number_of_trades(self, total_number_of_trades):
        self.total_number_of_trades = total_number_of_trades
        self.save()

    def update_total_number_of_winning_trades(self, total_number_of_winning_trades):
        self.total_number_of_winning_trades = total_number_of_winning_trades
        self.save()

    def update_total_number_of_losing_trades(self, total_number_of_losing_trades):
        self.total_number_of_winning_trades = total_number_of_losing_trades
        self.save()

    def update_largest_winning_trade(self, largest_winning_trade):
        self.largest_winning_trade = largest_winning_trade
        self.save()

    def update_largest_losing_trade(self, largest_losing_trade):
        self.largest_losing_trade = largest_losing_trade
        self.save()

    def update_trade_win_rate(self, trade_win_rate):
        self.trade_win_rate = trade_win_rate
        self.save()

    def update_avg_winning_trade(self, avg_winning_trade):
        if avg_winning_trade:
            self.avg_winning_trade = avg_winning_trade
            self.save()

    def update_avg_losing_trade(self, avg_losing_trade):
        if avg_losing_trade:
            self.avg_losing_trade = avg_losing_trade
            self.save()

    def update_starting_balance(self, new_value):
        self.starting_balance += new_value
        self.save()

    def update_total_profit_loss(self, new_value):
        self.total_profit_loss += new_value
        self.save()


class Trade(
    TimeStampedModel,
    ActivatorModel ,
    Model):

    """
    trading.Trade
    Store 1 Trade log in each post request from the User
    """

    class Meta:
        verbose_name = 'Trade'
        verbose_name_plural = 'Trades'
        ordering = ['created']

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    summary = models.ForeignKey(Summary, on_delete=models.CASCADE, null=True, blank=True)
    market = models.CharField(default="EURUSD", max_length=200)
    closed_position = models.DecimalField(max_digits=10, decimal_places=2)
    entry_price = models.FloatField()
    stop_loss_price = models.FloatField()
    take_profit_price = models.FloatField()
    risk_reward = models.CharField(max_length=200, null=True, blank=True)

    def save(self, *args, **kwargs):
        sl = self.stop_loss_price - self.entry_price
        tp = self.entry_price - self.take_profit_price
        r = round(tp /sl)
        self.risk_reward = f"1:{r}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.market} at {self.created}"