from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator
from django.contrib.postgres.fields import HStoreField, ArrayField

from djutil.models import TimeStampedModel

from utils import gen_hash, expires



class User(AbstractBaseUser, TimeStampedModel):
    """
    A custom user class that basically mirrors Django's `AbstractUser` class
    and doesn't force `first_name` or `last_name` with sensibilities for
    international names.

    http://www.w3.org/International/questions/qa-personal-names
    """
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    id = models.CharField(_('user id'), max_length=20, primary_key=True)
    first_name = models.CharField(_('first name'), max_length=254, blank=True, default="")
    middle_name = models.CharField(_('middle name'), max_length=254, blank=True, default="")
    last_name = models.CharField(_('last_name name'), max_length=254, blank=True, default="")
    username = models.CharField(_('username'), max_length=254, unique=True)
    email = models.EmailField(_('email address'), max_length=254)
    phone_regex = RegexValidator(regex='[0-9]{10,12}',
                                 message= _("Phone number must be entered in the format:"
                                            " '9999999999'. Up to 12 digits allowed."))
    phone_number = models.CharField(_('phone_number'), validators=[phone_regex], max_length=12, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, default="")
    dob = models.DateField(_('dob'), blank=True, default="9999-01-01")
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=False,
    help_text=_('Designates whether this user should be treated as active. Unselect it instead of deleting accounts.'))
    image = models.ImageField(upload_to="profile/image/", max_length=700, blank=True, null=True)
    social_profiles = HStoreField(blank=True, null=True)


    USERNAME_FIELD = 'email'

    def __unicode__(self):
        return str(self.id)+str( self.email)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        app_label = 'mysite'

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        parts = [self.first_name, self.middle_name, self.last_name]
        return " ".join(x for x in parts if x)

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name.strip()

    # def email_user(self, subject, message, from_email=None):
    #     """
    #     Sends an email to this User.
    #     """
    #     send_mail(subject, message, from_email, [self.email])

    def forgot_password(self, *args, **kwargs):
        """
        send random password and link the password edit form
        """

        User.password_change(self)
        super(User, self).save(*args, **kwargs)

    # def password_change(self):
    #     password = User.objects.make_random_password()
    #
    #     #Send random generated password and link to password edit form
    #     # Commenting this code as SMTP server not working
    #     ask_for_password_change(password, self.get_full_name(), self.email)
    #
    #     self.set_password(password)

    @property
    def is_superuser(self):
        return self.is_staff

    @property
    def is_admin(self):
        return self.is_staff

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    def get_perms(self):
        all_perms = []
        for group in self.groups.all():
            all_perms += group.permissions.all()
        return all_perms

    def get_perms_names(self):
        all_perms = []
        for group in self.groups.all():
            for perm in group.permissions.all():
                all_perms.append(str(perm.codename))
        return all_perms

    def get_all_groups_names(self):
        all_groups = []
        for group in self.groups.all():
            all_groups.append(str(group.name))
        return all_groups

    def get_allowed_categories_as_writer(self):
        categories = []
        for i in self.groups.filter(name__contains="writer"):
            categories.append(i.name[0:-len('-writer')])
        return categories

    # def get_allowed_categories_as_editor(self):
    #     categories = []
    #     for i in self.groups.filter(name__contains="editor"):
    #         categories.append(i.name[0:-len('-editor')])
    #
    #     # If user is editor of one category, he can act as editor(this append will be used to get all editorials)
    #     if len(categories):
    #         categories.append(EDITOR)
    #
    #     return categories

    def get_allowed_categories_as_editor_or_writer(self):
        categories = self.get_allowed_categories_as_writer()
        for i in self.get_allowed_categories_as_editor():
            if i in categories:
                pass
            categories.append(i)
        return categories

    def get_allowed_categories_as_editor_or_writer_for_listicles(self):
        """
        :return: category list allowed to show the editor or writer
        """
        categories = self.get_allowed_categories_as_writer()
        categories_editor = []
        for i in self.groups.filter(name__contains="editor"):
            categories_editor.append(i.name[0:-len('-editor')])

        for i in categories_editor:
            if i in categories:
                pass
            categories.append(i)
        return categories

    def is_cms_admin(self):
        return True if self.groups.filter(name__contains='admin') else False

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = gen_hash(expires())
        super(User, self).save(*args, **kwargs)


class Location(models.Model):
    """Location Model
    """
    city = models.CharField(max_length=50, blank=True, null=True, default=None)
    state = models.CharField(max_length=50, blank=True, null=True, default=None)
    country = models.CharField(max_length=50, blank=True, null=True, default=None)
    formatted_address = models.CharField(max_length=200, blank=True, null=True, default=None)
    latitude = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)

    class Meta:
        abstract = True
        app_label = 'mysite'


class Flat(Location):
    """

    """
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    # user = models.ForeignKey(User)
    user_fb_id = models.CharField(max_length=100, blank=True, null=True, default=None)
    user_fb_name = models.CharField(max_length=500, blank=True, null=True, default=None)
    price = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    vacancy = models.IntegerField(null=True, blank=True)
    message = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=1000, blank=True, null=True, default=None)
    publish_at = models.DateTimeField(_('Post Publish Date'), blank=True, null=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True, default=None)
    furnishing_type = models.CharField(max_length=100, blank=True, null=True, default=None)
    post_id = models.CharField(max_length=100, blank=True, null=True, default=None)
    is_available = models.BooleanField(default=True, blank=True)
    like_count = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, default="")

    def __unicode__(self):
        return self.post_id

    class Meta:
        app_label = 'mysite'

    def get_gender(self):
        """

        :param instance:
        :return:
        """

        gender_dict = {'M': 'Male', 'F': 'Female'}
        return gender_dict.get(self.gender)


