from django.db import models
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from workalendar.america import Brazil
from django.contrib.auth.models import User

class CalendarioEvento(models.Model):
    titulo = models.CharField(max_length=100, verbose_name="Título")
    descricao = models.TextField(verbose_name="Descrição")
    data_limite = models.DateField(verbose_name="Data")
    responsavelEvento = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    concluido = models.BooleanField(default=False)
    dataConclusao = models.DateField(null=True, blank=True)
    observacao = models.TextField(null=True, blank=True, verbose_name="Observação") 
    recorrencia = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.concluido and self.dataConclusao is None:
            self.dataConclusao = timezone.now().date()

        if self.pk == None:

            super().save(*args, **kwargs)

            if self.recorrencia == 'Mensal':
                last_month_of_year = 12

                for month in range(self.data_limite.month + 1, last_month_of_year + 1):
                    new_instance = self
                    new_instance.pk = None
                    new_instance.recorrencia = None
                    new_instance.concluido = False
                    new_instance.observacao = None
                    new_instance.data_limite = self.data_limite + relativedelta(months=month - self.data_limite.month)
                    new_instance.save()
            
            elif self.recorrencia == '15° dia útil':
                cal = Brazil()
                current_date = self.data_limite + relativedelta(months=1)
                current_month = current_date.month

                while current_month <= 12:
                    day = 1
                    working_days_count = 0
                    while working_days_count < 15:
                        if cal.is_working_day(current_date.replace(day=day)):
                            working_days_count += 1
                        day += 1

                    new_instance = self
                    new_instance.pk = None
                    new_instance.recorrencia = None
                    new_instance.concluido = False
                    new_instance.observacao = None
                    new_instance.data_limite = current_date.replace(day=day - 1)
                    current_date = current_date + relativedelta(months=1)
                    current_month += 1
                    new_instance.save()

            elif self.recorrencia == '7° dia útil':
                cal = Brazil()
                current_date = self.data_limite + relativedelta(months=1)
                current_month = current_date.month

                while current_month <= 12:
                    day = 1
                    working_days_count = 0
                    while working_days_count < 7:
                        if cal.is_working_day(current_date.replace(day=day)):
                            working_days_count += 1
                        day += 1

                    new_instance = self
                    new_instance.pk = None
                    new_instance.recorrencia = None
                    new_instance.concluido = False
                    new_instance.observacao = None
                    new_instance.data_limite = current_date.replace(day=day - 1)
                    current_date = current_date + relativedelta(months=1)
                    current_month += 1
                    new_instance.save()

        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo
