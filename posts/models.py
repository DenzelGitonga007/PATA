from django.db import models
from django.contrib.auth import get_user_model # to reference the user model
from django.core.validators import FileExtensionValidator, MaxValueValidator

# Create your models here.


# File name path
def upload_to(instance, filename):
    """Uploading the image to the path of username"""
    return 'missing_persons_photos/{}/{}'.format(instance.user.username, filename)


class MissingPerson(models.Model): # the missing persons details
    """The missing person model"""
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE) 
    name = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.ImageField(
        upload_to=upload_to, # upload path
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            MaxValueValidator(limit_value=8, message='File size must be no more than 8 MB.')
            ]
        )
    location = models.CharField(max_length=255)
    date_missing = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Stringify
    def __str__(self):
        """Stringify the name"""
        return self.name