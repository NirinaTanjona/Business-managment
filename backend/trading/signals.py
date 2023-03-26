from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models import Max, Min, Avg, Sum
from rest_framework.authtoken.models import Token
from .models import Trade, Summary

def action(user, summary, query):

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

    # get closed_position to populate total_profit_loss
    total_profit_loss = query.aggregate(Sum('closed_position'))['closed_position__sum']
    summary.update_total_profit_loss(total_profit_loss)



@receiver(post_save, sender=User, weak=False)
def report_uploaded(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
        # Summary.objects.create(user=instance)


@receiver(post_save, sender=Trade)
def update_summary(sender, instance, created, **kwargs):
    '''
    update the Summary model according to the value of all trade tables
    '''

    user = instance.user
    summary = instance.summary
    query = summary.trades.all()

    if created:
        # Get the user owner of the trade
        action(user, summary, query)
        # Update balance the same as balance in summary
        instance.update_balance(summary.balance)
    else:
        action(user, summary, query)


@receiver(post_delete, sender=Trade)
def update_summary(sender, instance, **kwargs):
    '''
    update the summary model when one trade got deleted
    '''
    user = instance.user
    summary = instance.summary
    query = summary.trades.all()
    if query.count():
        action(user, summary, query)
    else:
        summary.update_total_number_of_trades(0)
        summary.update_total_number_of_winning_trades(0)
        summary.update_total_number_of_losing_trades(0)
        summary.update_largest_winning_trade(0)
        summary.update_largest_losing_trade(0)
        summary.update_trade_win_rate("0%")
        summary.update_avg_winning_trade(0)
        summary.update_avg_losing_trade(0)
        summary.update_total_profit_loss(0)
