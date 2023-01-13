import datetime
import time

from celery import shared_task
from celery_singleton import Singleton
from django.db.models import F


@shared_task(base=Singleton)
def set_price(subscriprion_id):
    from services.models import Subscription

    time.sleep(5)

    subscribtion = Subscription.objects.filter(id=subscriprion_id).annotate(
        annotated_price=F('service__full_price') -
                        F('service__full_price') * F('plan__discount_percent') / 100.00).first()
    # new_price = (subscribtion.service.full_price -
    #              subscribtion.service.full_price * subscribtion.plan.discount_percent / 100)

    time.sleep(20)

    subscribtion.price = subscribtion.annotated_price
    subscribtion.save()


@shared_task(base=Singleton)
def set_comment(subscriprion_id):
    from services.models import Subscription

    subscribtion = Subscription.objects.get(id=subscriprion_id)

    time.sleep(27)

    subscribtion.comment = str(datetime.datetime.now())
    subscribtion.save()
