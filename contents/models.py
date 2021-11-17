from django.db import models
from django.db.models.deletion import CASCADE
from django.apps import apps
import importlib

class Content(models.Model):
    id = models.BigAutoField(primary_key=True)
    owner_id = models.ForeignKey(
        'owners.Owner',
        to_field='id',
        db_column='owner_id',
        on_delete=models.CASCADE
    )
    url = models.CharField(max_length=300, null=False, 
    # unique=True
    )
    title = models.CharField(max_length=200, null=False)
    author = models.CharField(max_length=40, null=True, blank=True)
    pub_date = models.CharField(max_length=50, null=True, blank=True)
    img_url = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return "<Content(id='%d', owner_id='%s', url='%s', title='%s', author='%s', pub_date='%s', img_url='%s', created_at='%s', updated_at='%s')>" % ( 
            self.id, self.owner_id, self.url, self.title, self.author, self.pub_date, self.img_url, self.created_at, self.updated_at)
    
# blank=True works wrt to Form validation
# Owner = apps.get_model('owners', 'Owner')
