from django.conf import settings
from django.core.cache import cache
from django.db.models import Prefetch, F, Sum
from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet

from clients.models import Client
from services.models import Subscription
from services.serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    # Проблема N+1 для клиентов решается prefetch_related, в запросе появляется ..."clients_client"."id" IN (1, 2);
    # Для email пользователя второй prefetch_related
    # queryset = Subscription.objects.all().prefetch_related(
    #     'client').prefetch_related('client__user')

    # Либо пишем при помощи класса, чтобы исключить ненужные поля в запросах (queryset в классе Prefetch)
    # Теперь не 3 а 2 запроса, пристствует INNER JOIN "auth_user"
    # queryset = Subscription.objects.all().prefetch_related(
    #     Prefetch('client', queryset=Client.objects.all()
    #              .select_related('user').only('company_name', 'user__email'))
    # )

    # Теперь, когда появился вложенный сериализатор
    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        Prefetch('client', queryset=Client.objects.all()
                 .select_related('user').only('company_name', 'user__email'))
    )  # .annotate(price=F('service__full_price') -
    #                 F('service__full_price') * F('plan__discount_percent') / 100.00)
    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        responce = super().list(request, *args, **kwargs)

        price_cache = cache.get(settings.PRICE_CACHE_NAME)

        if price_cache:
            total_price = price_cache
        else:
            total_price = queryset.aggregate(total=Sum('price')).get('total')
            cache.set(settings.PRICE_CACHE_NAME, total_price, 60 * 60)

        # Подменяем данные
        responce_data = {'result': responce.data}
        # Агрегируем наше виртуальное поле price,
        # которое мы создали в аннотациях и добавляем его в responce
        # queryset.aggregate(total=Sum('price')) это словать в котором лежит total
        responce_data['total_amount'] = total_price
        responce.data = responce_data

        return responce
