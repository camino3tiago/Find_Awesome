from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):   # AbstractUserより柔軟性あり
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)   # アカウントが有効か
    is_admin = models.BooleanField(default=False)   # 管理画面に入れるか

    objects = UserManager()

    USERNAME_FIELD = 'email'    # usernameをemailにする
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        'Does the user have a specific permission?'
        return True

    def has_module_perms(self, app_label):
        'Does the user have permissions to view the app "app_label"?'
        return True
    
    @property
    def is_staff(self):
        'Is the user a member of staff?'
        return self.is_admin

# ----- OneToOneField を同時に作成 -----
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)   # post_save(=Userを保存した直後)に、sender=Userでreceiver=Profileで下の処理を追加
def create_onetoone(sender, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance']) # Profileモデルのuserフィールド=kwargs['instance']
# ----- OneToOneField を同時に作成 -----



from django.db import models
from django.contrib.auth import get_user_model
import os

# instance, filenameを使用して、パスを生成する
def upload_image_to(instance, filename):
    user_id = str(instance.user.id)
    return os.path.join('image', user_id, filename)


class Profile(models.Model):    
    # Userが作成された時に、Profileも作成する⇨account_modelsのcreate_onetoone関数部分参照
    user = models.OneToOneField(    # user: profile = 1 : 1
        get_user_model(),
        unique=True,
        on_delete=models.CASCADE,
        primary_key=True        # userをそのままidにする
    )
    username = models.CharField(
        default="Anonymous",
        max_length=30,
    )
    country = models.CharField(
        default="",
        max_length=50,  
    )
    city = models.CharField(
        default="",
        blank=True,
        null=True,
        max_length=50,
    )
    age = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    hobby = models.CharField(
        max_length=100,
        default='',
        blank=True,
        null=True,
    )
    image = models.ImageField(
        default="",
        blank=True,
        upload_to=upload_image_to,
    )
    def __str__(self):
        return f'{self.username}'


