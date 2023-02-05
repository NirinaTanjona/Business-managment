from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models import Max, Min, Avg
from rest_framework.authtoken.models import Token
from .models import Trade, Summary

@receiver(post_save, sender=User, weak=False)
def report_uploaded(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
        Summary.objects.create(user=instance)

@receiver(post_save, sender=Trade)
def update_summary(sender, instance, created, **kwargs):
    '''
    update the Summary model according to the value of all trade tables
    '''
    if created:
        # Get the user owner of the trade
        user = instance.user
        summary = user.summary
        query = Trade.objects.filter(user=user).all()

        # set total number of trade corresponding to the user above
        summary.update_total_number_of_trades(query.count())

        # set total number of winning trade
        total_number_of_winning_trades = query.filter(closed_position__gt=0)
        summary.update_total_number_of_winning_trades(total_number_of_winning_trades.count())

        # set total number of losing trade
        total_number_of_losing_trades = query.filter(closed_position__lt=0)
        summary.update_total_number_of_losing_trades(total_number_of_losing_trades.count())

        # set the largest winning trade
        largest_winning_trade = query.aggregate(Max('closed_position'))['closed_position__max']
        summary.update_largest_winning_trade(largest_winning_trade)

        # set the largest losing trade
        largest_losing_trade = query.aggregate(Min('closed_position'))['closed_position__min']
        summary.update_largest_losing_trade(largest_losing_trade)

        # set the trade winrate
        trade_win_rate = int((total_number_of_winning_trades.count() / query.count()) * 100)
        summary.update_trade_win_rate(f"{str(trade_win_rate)}%")

        # set the avg_winning_trade
        avg_winning_trade = query.filter(closed_position__gt=0).aggregate(Avg('closed_position'))['closed_position__avg']
        summary.update_avg_winning_trade(avg_winning_trade)

        # set the avg_losing_trade
        avg_losing_trade = query.filter(closed_position__lt=0).aggregate(Avg('closed_position'))['closed_position__avg']
        summary.update_avg_losing_trade(avg_losing_trade)

        # get closed_position wich is profit or losse from the instance trade created
        new_value = instance.closed_position
        summary.update_starting_balance(new_value)

        # get closed_position to populate total_profit_loss
        new_value = instance.closed_position
        summary.update_total_profit_loss(new_value)
