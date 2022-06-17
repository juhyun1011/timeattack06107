from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email')
        user = self.model(
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

#유저타입
class UserType(models.Model):
    name = models.CharField("타입이름", max_length=20)

    def __str__(self):
        return self.name

# custom user model
class User(AbstractBaseUser):
    email = models.EmailField("이메일 주소", max_length=100, unique=True)
    password = models.CharField("비밀번호", max_length=128)
    fullname = models.CharField("이름", max_length=20)
    join_date = models.DateTimeField("가입일", auto_now_add=True)
    type =  models.ForeignKey('user.UserType', verbose_name="유저타입", on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True) 

    is_admin = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []
    
    objects = UserManager() # custom user 생성 시 필요
    
    def __str__(self):
        return self.email


    def has_perm(self, perm, obj=None):
        return True
    

    def has_module_perms(self, app_label): 
        return True
    

    @property
    def is_staff(self): 
        return self.is_admin





    def __str__(self):
        return self.name
