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
    name = models.CharField(max_length=50, verbose_name="Название")
    email = models.CharField(max_length=30, unique=True)

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"


class Product(models.Model):
    """Товар"""
    title = models.CharField(max_length=100, verbose_name="Название")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Category(models.Model):
    """Категория"""
    title = models.CharField(max_length=50, verbose_name="Название")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Parameter(models.Model):
    """Характеристика"""
    title = models.CharField(max_length=50, verbose_name="Название")

    class Meta:
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"


class ProductInfo(models.Model):
    """Информация о товаре"""
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        verbose_name="Поставщик",
        related_name="products_info"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар",
        related_name="products_info"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория",
        related_name="products_info"
    )
    parameters_info = models.ManyToManyField(
        Parameter,
        verbose_name="Характеристика",
        related_name="products_info",
        through="ParameterInfo"
    )
    price = models.PositiveIntegerField(
        verbose_name="Стоимость"
    )
    created_add = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания"
    )

    status = models.CharField(
        max_length=10,
        verbose_name="Статус",
        choices=STATUS_PRODUCT,
        default="CLOSED"
    )

    class Meta:
        verbose_name = "Информация о товаре"
        verbose_name_plural = "Информация о товарах"


class ParameterInfo(models.Model):
    """Описание характеристики"""
    parameter = models.ForeignKey(
        Parameter,
        verbose_name="Характеристика",
        on_delete=models.CASCADE
    )
    product_info = models.ForeignKey(
        ProductInfo,
        verbose_name="Информация о товаре",
        on_delete=models.CASCADE
    )
    description = models.TextField(verbose_name="Описание")

    class Meta:
        verbose_name = "Описание характеристики"
        verbose_name_plural = "Описания характеристик"


class Shop(models.Model):
    """Магазин"""
    name = models.CharField(max_length=50, verbose_name="Название")

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"


class Manager(models.Model):
    """Менеджер магазина"""
    name = models.CharField(max_length=30, verbose_name="Имя")
    email = models.CharField(max_length=30, unique=True)
    shop = models.ForeignKey(
        Shop,
        verbose_name="Магазин",
        related_name="manegers",
        on_delete=models.CASCADE
    )
    password = models.CharField(max_length=30, verbose_name="Пароль")

    class Meta:
        verbose_name = "Менеджер"
        verbose_name_plural = "Менеджеры"


class Order(models.Model):
    """Заказ"""
    manager = models.ForeignKey(
        Manager,
        verbose_name="Менеджер",
        related_name="orders",
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=10,
        verbose_name="Статус",
        choices=STATUS_ORDER,
        default="NEW"
    )
    products_info = models.ManyToManyField(
        ProductInfo,
        verbose_name="Информация о товаре",
        through='OrderPosition',
        related_name="orders"
    )
    created_add = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания"
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderPosition(models.Model):
    """Позиция в заказе"""
    order = models.ForeignKey(
        Order,
        verbose_name="Заказ",
        on_delete=models.CASCADE,
    )
    product_info = models.ForeignKey(
        ProductInfo,
        verbose_name="Информация о товаре",
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(
        verbose_name="Количество",
        validators=[MinValueValidator(1)],
        default=1
    )

    class Meta:
        verbose_name = "Позиция в заказе"
        verbose_name_plural = "Позиции в заказе"
