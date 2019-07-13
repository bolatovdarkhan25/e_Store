from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from transliterate import translit
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
# Create your models here.


class Brand(models.Model):
    name = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, default='')
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(translit(self.name, reversed=True))
        super(Category, self).save(*args, **kwargs)


class ProductManager(models.Manager):

    def all_available(self, *args, **kwargs):
        return super(ProductManager, self).get_queryset().filter(available=True)


def image_folder(instance, filename):
    filename = instance.slug + '.' + filename.split('.')[1]
    return "{}/{}".format(instance.slug, filename)


class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='')
    slug = models.CharField(max_length=255, default='', blank=True)
    image = models.ImageField(upload_to=image_folder, default='')
    params = models.TextField()
    price = models.DecimalField(max_digits=30, decimal_places=2)
    available = models.BooleanField(default=True)
    to_carousel = models.BooleanField(default=False)
    objects = ProductManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)
    item_total_price = models.DecimalField(max_digits=30, decimal_places=2, blank=True)

    def __str__(self):
        return 'Cart item for product {}'.format(self.product.name)

    def save(self, *args, **kwargs):
        if not self.item_total_price:
            self.item_total_price = self.product.price * self.amount
        super(CartItem, self).save(*args, **kwargs)


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem, blank=True)
    cart_total_price = models.DecimalField(max_digits=40, decimal_places=2)
    cart_total_amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.user)

    def add_to_cart(self, product_slug):
        cart = self
        product = Product.objects.get(slug=product_slug)
        new_item = ''
        try:
            if CartItem.objects.get(product=product, item_total_price=product.price):
                new_item = CartItem.objects.get(product=product, item_total_price=product.price)
        except:
            new_item = CartItem.objects.create(product=product, item_total_price=product.price, amount=1)
        if new_item not in cart.items.all():
            cart.items.add(new_item)
            cart.save()

    def remove_from_cart(self, product_slug):
        cart = self
        product = Product.objects.get(slug=product_slug)
        for cart_item in cart.items.all():
            if cart_item.product == product:
                cart.items.remove(cart_item)
                cart.save()


class Cart_Icon(models.Model):
    name = models.CharField(max_length=10, default='')
    slug = models.SlugField(max_length=10, default='', blank=True)
    image = models.ImageField(upload_to=image_folder, default='')

    def __str__(self):
        return self.name


ORDER_STATUS_CHOICES = (
    ('Принят в обработку', 'Принят в обработку'),
    ('Выполняется', 'Выполняется'),
    ('Оплачен', 'Оплачен'),
)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = ArrayField(models.CharField(max_length=255, default=''), default=list)
    address = models.CharField(max_length=255, default='', verbose_name='Адресс доставки*')
    buying_type = models.CharField(max_length=50, choices=(('Самовывоз', 'Самовывоз'), ('Доставка', 'Доставка')),
                                   default=('Самовывоз', 'Самовывоз'), verbose_name='Способ доставки*')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата получения*')
    comments = models.TextField(blank=True, verbose_name='Комментарии')
    status = models.CharField(max_length=255, choices=ORDER_STATUS_CHOICES, verbose_name='Статус заказа')

    def __str__(self):
        return "Заказ номер {}".format(str(self.id))