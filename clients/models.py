from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profiles(sender, instance, created, **kwargs):
    """При создании пользователя создаем UserProfile"""
    if created:
        from general.models import UserProfile
        UserProfile.objects.create(user=instance)

class Client(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name='client_profile',
        null=True,  # Добавьте временно
        blank=True
    )
    sphere = models.CharField("Сфера деятельности", max_length=100)
    company_name = models.CharField("Название компании", max_length=200, blank=True)
    
    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
    
    def __str__(self) -> str:
        return self.user.userprofile.fio or self.user.username

class Project(models.Model):
    name = models.CharField("Название проекта", max_length=200)
    client_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name="Клиент",
        related_name='projects',
        limit_choices_to={'client_profile__isnull': False}  # Только пользователи с профилем клиента
    )
    start_date = models.DateField("Дата начала", auto_now_add=True)
    deadline = models.DateField("Срок сдачи")
    budget = models.DecimalField("Бюджет", max_digits=10, decimal_places=2)
    status = models.CharField("Статус", max_length=50)  # Text choices - просто текст
    description = models.TextField("Описание проекта", blank=True)

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
    
    def __str__(self) -> str:
        return self.name

class Favour(models.Model):
    name = models.CharField("Название услуги", max_length=100)
    description = models.TextField("Описание услуги", blank=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    category = models.CharField("Категория", max_length=50)  # Убрали choices
    
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
    
    def __str__(self) -> str:
        return self.name
    




class Employee(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь", 
        related_name='employee_profile',
        null=True,  # Добавьте временно
        blank=True
    )
    position = models.CharField("Должность", max_length=50)
    start_work_date = models.DateField("Дата приёма на работу")
    
    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
    
    def __str__(self) -> str:
        profile_fio = self.user.userprofile.fio
        return f"{profile_fio} ({self.position})" if profile_fio else f"{self.user.username} ({self.position})"


class ProjectService(models.Model):
    project = models.ForeignKey(
        'Project', 
        on_delete=models.CASCADE, 
        verbose_name="Проект",
        related_name='project_services'
    )
    favour = models.ForeignKey(
        'Favour', 
        on_delete=models.CASCADE, 
        verbose_name="Услуга",
        related_name='project_services'
    )
    employee_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Ответственный сотрудник",
        null=True,
        blank=True,
        related_name='assigned_services',
        limit_choices_to={'employee_profile__isnull': False}  # Только сотрудники
    )
    status = models.CharField("Статус выполнения", max_length=50, default='in_progress')  # Text choices
    start_date = models.DateField("Дата начала работы", auto_now_add=True)
    end_date = models.DateField("Дата завершения", null=True, blank=True)
    hours_spent = models.DecimalField("Затрачено часов", max_digits=6, decimal_places=2, default=0)
    notes = models.TextField("Примечания", blank=True)

    class Meta:
        verbose_name = "Услуга в проекте"
        verbose_name_plural = "Услуги в проектах"
    
    def __str__(self) -> str:
        return f"{self.favour.name} - {self.project.name}"
    

class Review(models.Model):
    project = models.ForeignKey(
        'Project', 
        on_delete=models.CASCADE, 
        verbose_name="Проект",
        related_name='reviews'
    )
    rating = models.IntegerField("Оценка", default=5)  # Убрали choices
    feedback = models.TextField("Текст отзыва")
    created_at = models.DateTimeField("Дата отзыва", auto_now_add=True)
    is_published = models.BooleanField("Опубликован", default=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
    
    def __str__(self) -> str:
        return f"Отзыв на {self.project.name}"
    
    @property
    def client_user(self):
        """Клиент, оставивший отзыв"""
        return self.project.client_user