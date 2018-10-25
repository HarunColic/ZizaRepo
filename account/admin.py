from django.contrib import admin
from account import models as Amodels
from post import models as Pmodels

# Register your models here.

admin.site.register(Amodels.UserProfile)
admin.site.register(Amodels.Employee)
admin.site.register(Amodels.Company)
admin.site.register(Pmodels.Category)
admin.site.register(Pmodels.Post)
admin.site.register(Pmodels.PostCategories)
admin.site.register(Pmodels.WorkersPosts)
admin.site.register(Pmodels.UserCategories)
admin.site.register(Pmodels.Tag)
admin.site.register(Pmodels.FAQ)
admin.site.register(Pmodels.PostTags)


fields = ('CV_file', )
