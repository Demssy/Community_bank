from django.db import models

class Scholarship(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    Location = models.CharField(max_length=100)
    requirements = models.CharField(max_length=250)
    Amount = models.CharField(max_length=50)
    Hours = models.CharField(max_length=50)
    image = models.ImageField(upload_to="scholarship/images")

    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, path = self.image.storage, self.image.path
        # Delete the model before the file
        super(Scholarship, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)


    def __str__(self):
        return self.title


