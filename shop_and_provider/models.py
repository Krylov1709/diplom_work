from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


STATUS_PRODUCT = (
    ('CLOSED', 'Не доступно'),
    ('OPEN', 'Доступно')
)

STATUS_ORDER = (
    ('NEW', 'Новый'),
    ('COMPLETED', 'Завершенный'),
)


class Provider(models.Model):
    """Поставщик"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="providers",
        verbose_name="Пользователь"
    )
    title = models.CharField(
        max_length=50,
        verbose_name="Название",
        null=False,
        blank=False
    )
    company = models.CharField(
        max_length=30,
        verbose_name="Компания",
        unique=True,
        null=False,
        blank=False
    )
    email = models.EmailField(
        max_length=50,
        unique=True
    )
    created_add = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания"
    )

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"

    def __str__(self):
        return self.title


class Category(models.Model):
    """Категория"""
    title = models.CharField(
        max_length=50,
        verbose_name="Название",
        null=False,
        blank=False
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title


class Parameter(models.Model):
    """Характеристика"""
    title = models.CharField(
        max_length=50,
        verbose_name="Название",
        null=False,
        blank=False
    )

    class Meta:
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"

    def __str__(self):
        return self.title


class Product(models.Model):
    """Товар"""
    title = models.CharField(
        unique=True,
        max_length=100,
        verbose_name="Название",
        null=False,
        blank=False
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория",
        related_name="products"
    )
    parameters_info = models.ManyToManyField(
        Parameter,
        verbose_name="Характеристика",
        related_name="products",
        through="ParameterInfo"
    )
    created_add = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания"
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.title


class ParameterInfo(models.Model):
    """Описание характеристики"""
    parameter = models.ForeignKey(
        Parameter,
        verbose_name="Характеристика",
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        verbose_name="Товар",
        on_delete=models.CASCADE
    )
    description = models.TextField(
        verbose_name="Описание",
        null=False,
        blank=False
    )

    class Meta:
        verbose_name = "Описание характеристики"
        verbose_name_plural = "Описания характеристик"


class ProductProvider(models.Model):
    """Товар поставщика"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар",
        related_name="providers"
    )
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        verbose_name="Поставщик",
        related_name="products"
    )
    price = models.PositiveIntegerField(
        verbose_name="Стоимость",
        default=0
    )
    status = models.CharField(
        max_length=10,
        verbose_name="Статус",
        choices=STATUS_PRODUCT,
        default="CLOSED"
    )
    created_add = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания"
    )
    update_add = models.DateTimeField(
        auto_now=True,
        verbose_name="Время обновления"
    )

    class Meta:
        verbose_name = "Товар поставщика"
        verbose_name_plural = "Товары постащиков"

    def __str__(self):
        return f'{self.product.title} ({self.provider.title})'


class Shop(models.Model):
    """Магазин"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shops",
        verbose_name="Пользователь"
    )
    title = models.CharField(
        max_length=50,
        verbose_name="Название",
        null=False,
        blank=False
    )
    company = models.CharField(
        max_length=30,
        unique=True,
        null=False,
        blank=False
    )
    email = models.EmailField(
        max_length=50,
        unique=True
    )
    created_add = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания"
    )

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"

    def __str__(self):
        return self.title


class Order(models.Model):
    """Заказ"""
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        verbose_name="Магазин",
        related_name="orders"
    )
    status = models.CharField(
        max_length=10,
        verbose_name="Статус",
        choices=STATUS_ORDER,
        default="NEW"
    )
    products_provider = models.ManyToManyField(
        ProductProvider,
        verbose_name="Товары",
        through='OrderPosition',
        related_name="orders"
    )
    created_add = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания"
    )
    update_add = models.DateTimeField(
        auto_now=True,
        verbose_name="Время обновления"
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f'{self.id} ({self.shop})'


class OrderPosition(models.Model):
    """Позиция в заказе"""
    order = models.ForeignKey(
        Order,
        verbose_name="Заказ",
        on_delete=models.CASCADE
    )
    product_provider = models.ForeignKey(
        ProductProvider,
        verbose_name="Товар",
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(
        verbose_name="Количество",
        validators=[MinValueValidator(1)],
        default=1
    )

    class Meta:
        verbose_name = "Позиция в заказе"
        verbose_name_plural = "Позиции в заказе"

