import math
from django.db import models
from django.contrib.auth.models import User
from utils.model_abstracts import Model
from django_extensions.db.models import (
    TimeStampedModel,
    ActivatorModel,
    TitleSlugDescriptionModel
)


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
    market = models.CharField(default="EURUSD", max_length=200)
    closed_position = models.DecimalField(max_digits=10, decimal_places=2)
    entry_price = models.FloatField()
    stop_loss_price = models.FloatField()
    take_profit_price = models.FloatField()
    risk_reward = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        sl = self.stop_loss_price - self.entry_price
        tp = self.entry_price - self.take_profit_price
        r = round(tp /sl)
        self.risk_reward = f"1:{r}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.market} at {self.created}"

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
    total_number_of_trades = models.PositiveIntegerField(default=0)
    total_number_of_winning_trades = models.PositiveIntegerField(default=0)
    total_number_of_losing_trades = models.PositiveIntegerField(default=0)
    total_number_of_be_trade = models.PositiveIntegerField(default=0)
    largest_winning_trade = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    largest_losing_trade = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    trade_win_rate = models.CharField(max_length=10)
    avg_winning_trade = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    avg_losing_trade = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    total_trade_costs = models.DecimalField(default=0, max_digits=10, decimal_places=2)

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
        self.avg_winning_trade = avg_winning_trade
        self.save()
