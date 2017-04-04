from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


class Register(models.Model):
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    mobile = models.CharField(max_length=50)  
    image = models.ImageField(upload_to="polls/static/polls/images/", default='/static/polls/images/background.gif')

class ProductCategory(models.Model):
    name = models.CharField(max_length=200)
    parent_categ_id = models.ForeignKey('self', null=True, blank=True)
    sequence = models.DecimalField(max_digits=4, decimal_places=0, null=True, blank=True)

    def __str__(self):
        return self.name    

class ProductImage(models.Model): 
    product_image = models.ImageField(upload_to="polls/static/polls/images/", default='/static/polls/images/background.gif') 
    product_thumbnail_image = models.ImageField(upload_to="polls/static/polls/thumb_images/", null=True, blank=True) 
    name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=150)
    description = models.TextField()
    manufacturer = models.CharField(max_length=300,blank=True)
    price_in_dollars = models.DecimalField(max_digits=6,decimal_places=2) 
    product_categ_id = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return self.name


    def save(self):
        # create a thumbnail
        self.create_thumbnail()
        super(ProductImage, self).save()
    def create_thumbnail(self):
        # create a thumbnail
        #self.create_thumbnail()
        from PIL import Image
        from cStringIO import StringIO
        from django.core.files.uploadedfile import SimpleUploadedFile
        import os
        try:
            DJANGO_TYPE = self.image.file.content_type
            if DJANGO_TYPE == 'image/jpeg':
                PIL_TYPE = 'jpeg'
                FILE_EXTENSION = 'jpg'
            elif DJANGO_TYPE == 'image/png':
                PIL_TYPE = 'png'
                FILE_EXTENSION = 'png'
            else:
                print error
            print StringIO(self.image.read())
            im = Image.open(StringIO(self.image.read()))
            size = 128, 128
            im.thumbnail(size, Image.ANTIALIAS)
             # Save the thumbnail
            temp_handle = StringIO()
            im.save(temp_handle, PIL_TYPE)
            temp_handle.seek(0)
            # Save image to a SimpleUploadedFile which can be saved into
            # ImageField
            suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
            temp_handle.read(), content_type=DJANGO_TYPE)
            # Save SimpleUploadedFile into image field
            self.thumb.save('%s_thumbnail.%s'%(os.path.splitext(suf.name)[0],FILE_EXTENSION), suf, save=True)
        except Exception as e:
            print e


class BuyerDetail(models.Model): 
    buyer_name = models.CharField(max_length=150)
    buyer_email = models.CharField(max_length=150)
    buyer_mobile = models.CharField(max_length=150)
    buyer_address1 = models.CharField(max_length=150)
    buyer_address2 = models.CharField(max_length=150)
    buyer_pincode = models.CharField(max_length=150)
    buyer_city = models.CharField(max_length=150)
    buyer_state = models.CharField(max_length=150)
    buyer_country = models.CharField(max_length=150)



class Cart(models.Model):
    product_id = models.ForeignKey(ProductImage, on_delete=models.CASCADE, null=True)    
    price = models.DecimalField(max_digits=6,decimal_places=2)
    quantity = models.DecimalField(max_digits=6,decimal_places=2)
    register_id = models.ForeignKey(Register, null=True, blank=True)

