from django.db import models
from TM30_accounts.models import CustomUser
from django.forms import model_to_dict

class Item(models.Model):
    item_name = models.CharField(max_length=150, unique=True)
    price = models.FloatField(default=0.00)
    quantity_available = models.IntegerField(default=0)
    item_description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-item_name',)

    def __str__(self):
        return self.item_name

    @property
    def orders(self):
        return self.cart_item.all().values()

    @property
    def orders_count(self):
        return self.cart_item.all().values().count()

class Cart(models.Model):
    ITEM_STATUS = (
        ('pending', 'Pending'),
        ('delivered', 'Delivered'),
    )


    user = models.ForeignKey(CustomUser, related_name="user", on_delete=models.CASCADE)
    cart_item = models.ForeignKey(Item, related_name="cart_item", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    item_cost = models.FloatField(default=0.00)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=ITEM_STATUS, default='pending')

    def __str__(self): 
        return str(Item.objects.get(item_name=self.cart_item))

    @property
    def cart_content(self):
        return model_to_dict(self.cart_item, fields=['item_name', 'price'])


