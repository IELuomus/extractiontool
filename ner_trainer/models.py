from django.db import models

class TraitnameLearnData(models.Model):
    user_id = models.IntegerField(null=True)
    data = models.JSONField()

    # def _str_(self):
    #     return self.title
    
    # def delete(self, *args, **kwargs):
    #     self.TraitNameLearnData.delete()
    #     super().delete(*args, **kwargs)

    # ContactInfo.objects.filter(
    #     data__name='John',
    #     data__pets__has_key='dogs',
    #     data__cities__contains='London',
    # ).delete()
