from django.db import models
from accounts.models import Profile
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

# Create your models here.


class InvestorAccount(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=400, blank=True, null=True)
    investor_id = models.CharField(max_length=125, default='')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.savings_id or ''


@receiver(pre_save, sender=InvestorAccount)
def update_investor_id(sender, instance, **kwargs):
    # ledger balance
    instance.available_balance = instance.ledger_balance - \
                                 instance.savings_product.min_balance_for_withdrawal
    if not instance.savings_id:
        last_obj = InvestorAccount.objects.last()
        # print(last_obj.savings_id)
        if last_obj:
            if last_obj.savings_id:
                instance.savings_id = str(int(last_obj.savings_id) + 1)
        else:
            instance.savings_id = str(10000001)


class InvestorDocuments(models.Model):
    investor_account = models.ForeignKey(InvestorAccount, on_delete=models.CASCADE)
    file = models.FileField(upload_to='investor_documents')


class InvestorInvitation(models.Model):
    investor_account = models.ForeignKey(InvestorAccount, on_delete=models.CASCADE, 
    blank=True, null=True)
    accepted = models.BooleanField(default=False)
