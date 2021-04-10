from django.db import models

# class TraitnameData(models.Model):
#     data = models.JSONField()

# TraitnameData.objects.create(data={
#     'name': 'John',
#     'cities': ['London', 'Cambridge'],
#     'pets': {'dogs': ['Rufus', 'Meg']},
# })
# ContactInfo.objects.filter(
#     data__name='John',
#     data__pets__has_key='dogs',
#     data__cities__contains='London',
# ).delete()
