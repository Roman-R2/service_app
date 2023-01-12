from celery import shared_task
from django.db.models import F


@shared_task
def set_price(subscriprion_id):
    from services.models import Subscription

    subscribtion = Subscription.objects.filter(id=subscriprion_id).annotate(
        annotated_price=F('service__full_price') -
              F('service__full_price') * F('plan__discount_percent') / 100.00).first()
    # new_price = (subscribtion.service.full_price -
    #              subscribtion.service.full_price * subscribtion.plan.discount_percent / 100)
    subscribtion.price = subscribtion.annotated_price
    subscribtion.save()
