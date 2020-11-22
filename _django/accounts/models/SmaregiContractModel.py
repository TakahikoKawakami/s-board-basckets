from django.db import models
from django.utils.translation import gettext_lazy as _

class SmaregiContract(models.Model):
    """for smaregi contarct data"""
    
    conrtact_id = models.CharField(
        _('conrtarct id'),
        max_length=150,
        unique=True,
    )
    creator = models.CharField()
    modifier = models.CharField()
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    
    
    def __str__(self):
        return self.conrtact_id
