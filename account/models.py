from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from PIL import Image, ImageDraw, ImageFont
import os 
from django.core.files import File
from django.conf import settings


from django.db import models
from django.contrib.auth.models import User
from PIL import Image, ImageDraw, ImageFont
import os

def profile_picture_path(instance, filename):
    return f"profile_pictures/{instance.user.username}.png"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to=profile_picture_path, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Generate the profile picture if not already set
        if not self.profile_picture:
            self.generate_profile_picture()
        super().save(*args, **kwargs)

    def generate_profile_picture(self):
        initials = ''.join([part[0].upper() for part in self.user.get_full_name().split()[:2]]) or self.user.username[:2].upper()
        img_size = (200, 200)
        background_color = "#3498db"
        text_color = "white"

        image = Image.new("RGB", img_size, background_color)
        draw = ImageDraw.Draw(image)
        font_size = 100
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        # Use textbbox to calculate text dimensions
        bbox = draw.textbbox((0, 0), initials, font=font)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        text_position = ((img_size[0] - text_width) // 2, (img_size[1] - text_height) // 2)

        draw.text(text_position, initials, fill=text_color, font=font)

        # Save the image to the profile picture field
        image_path = os.path.join('media', profile_picture_path(self, "profile_picture.png"))
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        image.save(image_path)
        self.profile_picture.name = profile_picture_path(self, "profile_picture.png")