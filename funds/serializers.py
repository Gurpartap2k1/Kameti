from rest_framework import serializers
from .models import ChitFund

class ChitFundSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChitFund
        fields = '__all__'
        read_only_fields = ['host', 'fund_id', 'invite_token', 'is_active', 'created_at', 'members']

    def create(self, validated_data):
        fund = ChitFund.objects.create(**validated_data)
        fund.members.add(self.context['request'].user)  # Automatically add host as member
        return fund


from accounts.models import CustomUser


class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email']

class ChitFundSummarySerializer(serializers.ModelSerializer):
    members = UserSummarySerializer(many=True, read_only=True)
    host = UserSummarySerializer(read_only=True)

    class Meta:
        model = ChitFund
        fields = ['id', 'name', 'total_amount', 'duration_months', 'is_active', 'host', 'members']