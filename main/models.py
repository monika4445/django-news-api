from django.db import models

# a separate Tag model for using Many-to-Many relationship to associate multiple tags with multiple news articles
class Tag(models.Model): 
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/')  # For now I want to store images locally. Later on I can use S3Boto3Storage
                                                         # provided by the 'django-storages' package and configure my project to use Amazon S3
    tags = models.ManyToManyField(Tag)
    #tags = models.ForeignKey(Tag, on_delete=models.CASCADE) 
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if self.image:
            self.image_url = self.image.url
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title