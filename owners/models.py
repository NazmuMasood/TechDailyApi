from django.db import models
from django.db.models.deletion import CASCADE

class Owner(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20, null=False)
    url = models.CharField(max_length=100, null=False, unique=True)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return "<Owner(id='%d', name='%s', url='%s', created_at='%s', updated_at='%s')>" % ( 
            self.id, self.name, self.url, self.created_at, self.updated_at)

# blank=True works wrt to Form validation