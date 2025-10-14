from django.db import models

class Client(models.Model):
    name = models.CharField("ФИО", max_length=200)
    email = models.EmailField("Почта")
    sphere = models.CharField("Сфера деятельности", max_length=100)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
    
    def __str__(self) -> str:
        return self.name


class Project(models.Model):
    STATUS_CHOICES = [
        ('planning', 'Планирование'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершен'),
        ('on_hold', 'Приостановлен'),
    ]
    name = models.CharField("Название проекта", max_length=200)
    client = models.ForeignKey('Client', on_delete=models.CASCADE, null=True)
    start_date = models.DateField("Дата начала", auto_now_add=True)
    deadline = models.DateField("Срок сдачи")
    budget = models.DecimalField("Бюджет", max_digits=10, decimal_places=2)
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='planning')
    description = models.TextField("Описание проекта", blank=True)

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
    
    def __str__(self) -> str:
        return self.name
    
    
class Favour(models.Model):
    CATEGORY_CHOICES = [
        ('design', 'Дизайн'),
        ('programming', 'Разработка'),
        ('marketing', 'Маркетинг'),
        ('promotion', 'Реклама'),
    ]
    name = models.CharField("Название услуги", max_length=100)
    description = models.TextField("Описание услуги", blank=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    category = models.CharField("Категория", choices=CATEGORY_CHOICES)
    
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self) -> str:
        return self.name

class Employee(models.Model):
    name = models.CharField("ФИО", max_length=200)
    position = models.CharField("Должность", max_length=50)
    email = models.EmailField("Почта")
    start_work_date = models.DateField("Дата приёма на работу")
    
    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
    
    def __str__(self) -> str:
        return self.name

class ProjectService(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'Выполняется'),
        ('approval', 'Согласуется'),
        ('review', 'На проверке'),
        ('revision', 'Доработка'),
        ('completed', 'Выполнена'),
    ]
    
    project = models.ForeignKey('Project', on_delete=models.CASCADE, null=True )
    favour = models.ForeignKey('Favour', on_delete=models.CASCADE, null=True )
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, null=True)
    status = models.CharField(
        "Статус выполнения", 
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='in_progress'
    )
    start_date = models.DateField("Дата начала работы")
    end_date = models.DateField("Планируемая дата завершения", null=True, blank=True)
    notes = models.TextField("Примечания", blank=True)

    class Meta:
        verbose_name = "Услуга в проекте"
        verbose_name_plural = "Услуги в проектах"
    
    def __str__(self) -> str:
        return f"{self.favour.name} - {self.project.name}"
    

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - Очень плохо'),
        (2, '2 - Плохо'),
        (3, '3 - Удовлетворительно'),
        (4, '4 - Хорошо'),
        (5, '5 - Отлично'),
    ]
    
    project = models.ForeignKey('Project', on_delete=models.CASCADE, null=True)
    rating = models.IntegerField("Оценка", choices=RATING_CHOICES, default=5)
    feedback = models.TextField("Текст отзыва")
    created_at = models.DateField("Дата отзыва")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
    
    def __str__(self) -> str:
        return f"Отзыв на {self.project.name} ({self.rating}/5)"
    
    @property
    def client_name(self):
        """Имя клиента из связанного проекта"""
        return self.project.client.name if self.project.client else "Не указан"
    
    @property
    def client_email(self):
        """Email клиента из связанного проекта"""
        return self.project.client.email if self.project.client else "Не указан"
        
