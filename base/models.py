from django.db import models
import uuid


class BaseModel(models.Model):
    u_id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

