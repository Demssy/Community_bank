from django.db import models

class Scolarship(models.Model):
    title = models.TextField()
    content = models.TextField()
    Location = models.TextField()
    included = models.TextField()
    Amount = models.TextField()
    Hours = models.TextField()
    image = models.ImageField(upload_to="blog/images")


    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, path = self.image.storage, self.image.path
        # Delete the model before the file
        super(Project, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)


    def __str__(self):
        return self.title


