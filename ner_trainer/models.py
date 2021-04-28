from django.db import models
from users.models import User

class TraitnameLearnData(models.Model):
    user_id = models.IntegerField(null=True)
    data = models.JSONField()

    def _str_(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        self.TraitNameLearnData.delete()
        super().delete(*args, **kwargs)

