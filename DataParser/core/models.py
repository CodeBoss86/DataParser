from django.db import models

class ProductData(models.Model):
    ident = models.TextField(null=True)
    store_id = models.IntegerField(null=True)
    previous_price = models.IntegerField(null=True)
    price = models.IntegerField(null=True)
    currency = models.CharField(max_length=8, null=True)
    offer_description = models.TextField(null=True)
    manufacturersku = models.TextField(null=True)
    eankod = models.TextField(null=True)
    additional_info = models.TextField(null=True)
    producturl = models.TextField(null=True)
    stock = models.IntegerField(null=True)

    def __str__(self):
        desc = self.offer_description
        return desc