from django.db import models

class ProductData(models.Model):
    ident = models.TextField(null=True)
    store_id = models.TextField(null=True)
    previous_price = models.TextField(null=True)
    price = models.TextField(null=True)
    currency = models.TextField(null=True)
    offer_description = models.TextField(null=True)
    manufacturersku = models.TextField(null=True)
    eankod = models.TextField(null=True)
    additional_info = models.TextField(null=True)
    producturl = models.TextField(null=True)
    stockstatus = models.TextField(null=True)

    def __str__(self):
        desc = self.offer_description
        return desc

    def get_absolute_url(self):
        return self.producturl