import datetime
import time

from celery import shared_task
from celery_singleton import Singleton
from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from django.db.models import F


@shared_task(base=Singleton)
def set_price(subscriprion_id):
    from services.models import Subscription

    with transaction.atomic():
        subscribtion = Subscription.objects.select_for_update().filter(id=subscriprion_id).annotate(
            annotated_price=F('service__full_price') -
                            F('service__full_price') * F('plan__discount_percent') / 100.00).first()
        # new_price = (subscribtion.service.full_price -
        #              subscribtion.service.full_price * subscribtion.plan.discount_percent / 100)

        subscribtion.price = subscribtion.annotated_price
        subscribtion.save()

    cache.delete(settings.PRICE_CACHE_NAME)


@shared_task(base=Singleton)
def set_comment(subscriprion_id):
    from services.models import Subscription

    with transaction.atomic():
        subscribtion = Subscription.objects.select_for_update().get(id=subscriprion_id)

        subscribtion.comment = str(datetime.datetime.now())
        subscribtion.save()
    cache.delete(settings.PRICE_CACHE_NAME)
