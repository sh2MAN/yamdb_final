from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Title(models.Model):
    name = models.CharField('Название', max_length=100, db_index=True)
    year = models.PositiveSmallIntegerField('Год')
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        related_name='categories',
        verbose_name='Категория',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        'Genre',
        related_name='genres',
        blank=True,
        verbose_name='Жанр'
    )
    description = models.TextField('Описание', null=True, blank=True)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-id',)

    def __str__(self):
        return self.name


class BaseForCategoryGenre(models.Model):
    name = models.CharField('Наименование', max_length=20, db_index=True)
    slug = models.SlugField(max_length=20, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Category(BaseForCategoryGenre):
    pass

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(BaseForCategoryGenre):
    pass

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class BaseForCommAndRev(models.Model):
    text = models.TextField('текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)ss',
        verbose_name='автор'
    )
    pub_date = models.DateTimeField(
        auto_now=True,
        verbose_name='дата создания'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.text


class Review(BaseForCommAndRev):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение'
    )
    score = models.PositiveSmallIntegerField(
        'оценка', validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]


class Comment(BaseForCommAndRev):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='отзыв'
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
