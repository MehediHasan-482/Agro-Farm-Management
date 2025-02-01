from django.db import models

# Create your models here.
from django.db import models

class Portfolio(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    vision = models.TextField(null=True, blank=True)  # Vision for the farm management
    mission = models.TextField(null=True, blank=True)  # Mission for the farm management
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # For documents related to the portfolio (e.g., PDFs, word files)
    document = models.FileField(upload_to='portfolio_documents/', null=True, blank=True)

    # Framework image related to the management process
    framework_image = models.ImageField(upload_to='portfolio_images/', null=True, blank=True)

    # Health monitoring process document
    health_monitoring_document = models.FileField(upload_to='health_documents/', null=True, blank=True)

    # Animal health monitoring image (could be a diagram or process flow)
    health_monitoring_image = models.ImageField(upload_to='health_monitoring_images/', null=True, blank=True)

    def __str__(self):
        return self.title
