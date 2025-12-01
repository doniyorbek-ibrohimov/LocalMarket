from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg
from users.models import User

# --- Category ---
class Banner(models.Model):
    title = models.CharField(max_length=31)
    image = models.ImageField(upload_to='banners/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=31)
    banner = models.ForeignKey(Banner, on_delete=models.SET_NULL, null=True, related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)


# --- Product ---
class Product(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(validators=[MinValueValidator(0.0)])
    amount = models.PositiveSmallIntegerField()
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0),], default=0.0
    )
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)

    def update_rating(self):
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        self.rating = round(avg, 1)
        self.save(update_fields=["rating"])


    def get_active_discount(self):
        """Return the active discount object if any, otherwise None."""
        now = timezone.now()
        return (
            self.discounts.filter(
                active=True,
                start_date__lte=now,
                end_date__gte=now
            ).order_by('-percentage').first()
        )

    @property
    def discounted_price(self):
        """Return price with applied discount, if active."""
        discount = self.get_active_discount()
        if discount:
            discounted_value = self.price * (1 - discount.percentage / 100)
            return round(discounted_value, 2)
        return self.price


    def __str__(self):
        return self.name


class Discount(models.Model):
    title = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='discounts')
    percentage = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()
        if self.end_date <= self.start_date:
            raise ValidationError("End date must be after Start date!")
        overlapping = Discount.objects.filter(
            product = self.product,
            active = True,
            start_date__lte = self.end_date,
            end_date__gte = self.start_date,
        ).exclude(pk=self.pk)

        if overlapping.exists():
            raise ValidationError("Another active discount overlaps for this product")

    def __str__(self):
        return f"{self.title} - {self.percentage}%"

class Image(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='images/products')

    def __str__(self):
        return self.product.name

class Wishlist(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='withlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_user_product')
        ]

    def __str__(self):
        return f"{self.user.username} -> {self.product.name}"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rating = models.SmallIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


# --- Cart ---
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        return sum(item.total_price() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.discounted_price * self.quantity


