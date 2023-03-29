from collections import OrderedDict
from .models import Trade, Summary
from rest_framework_json_api import serializers
from rest_framework import status
from rest_framework.exceptions import APIException


class TradeSerializer(serializers.ModelSerializer):


    class Meta:
        model = Trade
        exclude = ('user', 'summary',)
        source = 'trades'


class ChartDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trade
        fields = ['modified', 'balance']


class SummarySerializer(serializers.ModelSerializer):

    # trades = TradeSerializer(many=True)

    class Meta:
        model = Summary
        fields = (
            'name',
            'starting_balance',
            'balance',
            'total_number_of_trades',
            'total_number_of_winning_trades',
            'total_number_of_losing_trades',
            'total_number_of_be_trade',
            'largest_winning_trade',
            'largest_losing_trade',
            'avg_winning_trade',
            'avg_losing_trade',
            'total_trade_costs',
            'total_profit_loss',
            'average_profit_loss_per_trade',
            'return_of_investment',
            'average_risk_reward',
            'average_risk_per_trade',
            'average_reward_per_trade',
            'trade_win_rate',
            # 'trades',
        )
        # extra_kwargs = {'trades': {'required': False, 'allow_null': True}}
