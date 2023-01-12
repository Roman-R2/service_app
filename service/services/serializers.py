from rest_framework import serializers

from services.models import Subscription, Plan


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ('__all__')


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()
    client_name = serializers.CharField(source='client.company_name')
    email = serializers.CharField(source='client.user.email')
    # имя поля price важно,
    # так как SerializerMethodField ищет метод get_price с префиксом get_
    price = serializers.SerializerMethodField()

    # instance это конкретная модель подписки (Subscription),
    # которую мы обрататываем в этом сериалайзере
    def get_price(self, instance):
        # return (instance.service.full_price
        #         - instance.service.full_price
        #         * (instance.plan.discount_percent / 100))
        return instance.price

    class Meta:
        model = Subscription
        fields = ('id', 'plan_id', 'client_name', 'email', 'plan', 'price')
