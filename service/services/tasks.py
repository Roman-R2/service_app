from celery import shared_task


@shared_task
def set_price(subscriprion_id):
    from services.models import Subscription

    subscribtion = Subscription.objects.get(id=subscriprion_id)
    new_price = (subscribtion.service.full_price -
                 subscribtion.service.full_price * subscribtion.plan.discount_percent / 100)
    subscribtion.price = new_price
    subscribtion.save()
