import uuid

from django.db import models
from django_lifecycle import LifecycleModelMixin, hook

class BaseModel(LifecycleModelMixin, models.Model):
	id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
	created_at  = models.DateTimeField(verbose_name='Registrado em', auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name='Atualizado em', auto_now=True)

	class Meta:
		abstract = True    

class Newsletter(BaseModel):
    email = models.EmailField(max_length=254, unique=True)
    subscription_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email