import math
from decimal import *
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
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)
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
    return_of_investment = models.CharField(default='0%', max_length=200)
    average_risk_reward = models.CharField(default='1:1', max_length=200)
    average_risk_per_trade = models.CharField(default='0%', max_length=200)
    average_reward_per_trade = models.CharField(default='0%', max_length=200)
    trade_win_rate = models.CharField(default='0%', max_length=200)

    def update_total_number_of_trades(self, total_number_of_trades):
        self.total_number_of_trades = total_number_of_trades
        self.save()

    def update_total_number_of_winning_trades(self, total_number_of_winning_trades):
        self.total_number_of_winning_trades = total_number_of_winning_trades
        self.save()

    def update_total_number_of_losing_trades(self, total_number_of_losing_trades):
        self.total_number_of_losing_trades = total_number_of_losing_trades
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
        else:
            self.avg_winning_trade = 0
        self.save()

    def update_avg_losing_trade(self, avg_losing_trade):
        if avg_losing_trade:
            self.avg_losing_trade = avg_losing_trade
        else:
            self.avg_losing_trade = 0
        self.save()

    def update_balance(self, new_balance):
        self.balance = new_balance
        self.save()

    def set_starting_balance(self, starting_balance):
        self.starting_balance = starting_balance
        self.save()

    def update_total_profit_loss(self, total_profit_loss):
        self.total_profit_loss = total_profit_loss
        self.save()

    def save(self, *args, **kwargs):
        if self.total_number_of_trades:
        # update the average profit loss per trade value by other field in the save model
            self.average_profit_loss_per_trade = self.total_profit_loss / self.total_number_of_trades
        else:
            self.average_profit_loss_per_trade = 0

        # update return of investment field (accumulated P/L + starting balance) / starting balance * 100
        if self.total_profit_loss:
            roi = (self.total_profit_loss / self.starting_balance) * 100
            self.return_of_investment = f"{round(roi, 2)}%"
        else:
            self.return_of_investment = "0%"

        # update balance by adding the profit and loss to the starting balance
        self.balance = self.starting_balance + self.total_profit_loss

        # update the average risk per trade in each trade created
        # (average losing trade / balance) * 100
        if self.balance:
            average_risk_per_trade = round((self.avg_losing_trade / self.balance) * 100, 2)
            self.average_risk_per_trade = f"{average_risk_per_trade}%"
        else:
            self.average_risk_per_trade = "0%"

        # update the average reward per trade in each trade created
        # (average winning trade / balance) * 100
        if self.balance:
            average_reward_per_trade = round((self.avg_winning_trade / self.balance) * 100, 2)
            self.average_reward_per_trade = f"{average_reward_per_trade}%"
        else:
            self.average_reward_per_trade = "0%"

        # update the average risk reward in each trade created
        # (average winning trade / average losing trade) * 100
        avg_risk_reward = 0
        if self.avg_winning_trade and self.avg_losing_trade:
            avg_risk_reward = round((self.avg_winning_trade / abs(self.avg_losing_trade)), 2)
        elif self.avg_winning_trade == 0:
            avg_risk_reward = 0
        elif self.avg_losing_trade == 0:
            avg_risk_reward = self.avg_winning_trade

        self.average_risk_reward = f"1:{avg_risk_reward}"

        super().save(*args, **kwargs)


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
    summary = models.ForeignKey(Summary, related_name='trades', on_delete=models.CASCADE, null=True, blank=True)
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    market = models.CharField(default='EURUSD', max_length=200)
    direction = models.CharField(default='SHORT', max_length=200)
    closed_position = models.DecimalField(max_digits=10, decimal_places=2)
    entry_price = models.FloatField(default=0)
    stop_loss_price = models.FloatField(default=0)
    take_profit_price = models.FloatField(null=True, blank=True)
    actual_exit_price = models.FloatField(default=0)
    risk_reward = models.CharField(max_length=200, null=True, blank=True)
    screen_before = models.URLField(null=True, blank=True)
    screen_after = models.URLField(null=True, blank=True)
    trade_notes = models.TextField(null=True, blank=True)
    discipline_rating = models.IntegerField(null=True, blank=True)
    emotional_state_of_mind = models.TextField(null=True, blank=True)

    def update_balance(self, new_balance):
        self.balance = new_balance
        self.save()

    def save(self, *args, **kwargs):
        sl = self.stop_loss_price - self.entry_price
        tp = self.entry_price - self.actual_exit_price
        r = round(tp /sl)
        self.risk_reward = f"1:{r}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.market} at {self.created}"