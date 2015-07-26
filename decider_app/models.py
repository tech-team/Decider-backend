# coding=utf-8
import hashlib
import uuid
from datetime import timedelta
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


def get_random_uid():
    return uuid.uuid4().hex


class MyUserManager(BaseUserManager):

    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          uid=get_random_uid(),
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, *args, **kwargs):
        if 'uid' in kwargs:

            social_site_id = SocialSite.objects.get(name='vk').id
            social_id = kwargs.get('uid')

            try:
                user = User.objects.get(social_site_id=social_site_id, social_id=social_id)
            except User.DoesNotExist:
                now = timezone.now()
                user = self.model(uid=get_random_uid(),
                                  social_id=social_id,
                                  social_site_id=social_site_id,
                                  is_active=True,
                                  last_login=now, date_joined=now)
                user.email = user.uid
                user.set_password(user.get_dummy_password())
                user.save(using=self._db)

            return user
        else:
            return self._create_user(*args, **kwargs)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password,
                                 True, True, **extra_fields)


class SocialSite(models.Model):
    class Meta:
        verbose_name = _(u'Социальный сайт')
        verbose_name_plural = _(u'Социальные сайты')
        ordering = ('name', )
        db_table = "d_social_site"

    name = models.CharField(max_length=20, verbose_name=u'Название')

    def __unicode__(self):
        return self.name


class Country(models.Model):
    class Meta:
        verbose_name = _(u'Страна')
        verbose_name_plural = _(u'Страны')
        ordering = ('name', )
        db_table = "d_country"

    name = models.CharField(max_length=100, verbose_name=u'Название')

    def __unicode__(self):
        return self.name


class Picture(models.Model):
    class Meta:
        verbose_name = _(u'Картинка')
        verbose_name_plural = _(u'Картинки')
        ordering = ('date_uploaded', )
        db_table = "d_picture"

    uid = models.CharField(max_length=100, unique=True, verbose_name=u'Уникальный идентификатор')
    url = models.CharField(max_length=255, verbose_name=u'Адрес картинки')
    preview_url = models.CharField(max_length=255, verbose_name=u'Адрес превью', null=True, blank=True)
    date_uploaded = models.DateTimeField(default=timezone.now, verbose_name=u'Дата загрузки')


class User(AbstractBaseUser, PermissionsMixin):

    objects = MyUserManager()

    USERNAME_FIELD = 'uid'

    class Meta:
        verbose_name = _(u'Пользователь')
        verbose_name_plural = _(u'Пользователи')
        ordering = ('-date_joined', )
        db_table = "d_user"
        unique_together = ('social_site', 'social_id',)

    email = models.EmailField(_('email address'), max_length=100, default=True, null=True, unique=True)
    uid = models.CharField(_('unique id for user'), max_length=50, unique=True, db_index=True)
    social_site = models.ForeignKey(SocialSite, blank=True, null=True)
    social_id = models.CharField(_('social site id'), max_length=100, blank=True, null=True)

    username = models.CharField(_('username'), max_length=50, blank=True, default='', db_index=True)
    first_name = models.CharField(_('first name'), max_length=50, blank=True, default='')
    last_name = models.CharField(_('last name'), max_length=50, blank=True, default='')
    middle_name = models.CharField(_('middle_name'), max_length=50, blank=True, default='')

    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    is_anonymous = models.BooleanField(default=False)

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_active = models.DateTimeField(_(u'Последняя активность'), default=timezone.now)

    birthday = models.DateField(_(u'День рождения'), blank=True, null=True)

    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.CharField(_(u'Город'), max_length=50, blank=True)
    about = models.TextField(_(u'О себе'), max_length=1000, blank=True)
    gender = models.NullBooleanField(_(u'Пол'), blank=True, null=True, default=None)

    avatar = models.OneToOneField(Picture, blank=True, null=True)

    def __unicode__(self):
        return self.email

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        full_name = '%s %s %s' % (self.first_name, self.middle_name, self.last_name)
        return full_name.strip()

    def get_dummy_password(self):
        return hashlib.md5(self.uid).hexdigest()

    def update_last_active(self):
        self.last_active = timezone.now()
        self.save()

    def registration_finished(self):
        return self.username != '' and User.objects.filter(username=self.username).count() == 1


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'Название', null=True, blank=True)

    class Meta:
        verbose_name = _(u'Категория')
        verbose_name_plural = _(u'Категории')
        db_table = "d_category"

    def __unicode__(self):
        return unicode(self.id) + '.' + (self.name if self.name else '')


class Question(models.Model):
    class Meta:
        verbose_name = _(u'Вопрос')
        verbose_name_plural = _(u'Вопросы')
        ordering = ('-creation_date', )
        db_table = "d_question"

    text = models.TextField(_(u'Текст вопроса'), max_length=500, blank=True, default='')
    is_closed = models.BooleanField(_(u'Закрыт?'), default=False)
    is_anonymous = models.BooleanField(_(u'Анонимен?'), default=False)
    creation_date = models.DateTimeField(_(u'Дата создания'), default=timezone.now)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="liked_questions")
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    share_image = models.ForeignKey(Picture, null=True, blank=True)

    comments_count = models.IntegerField(_(u'Количество комментов'), default=0)
    likes_count = models.IntegerField(_(u'Количество лайков'), default=0)

    is_active = models.BooleanField(default=True)
    spam_count = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return "Question #" + str(self.id) + " by " + self.author.uid


class Comment(models.Model):
    class Meta:
        verbose_name = _(u'Комментарий')
        verbose_name_plural = _(u'Комментарии')
        db_table = "d_comment"

    text = models.TextField(_(u'Текст комментария'), max_length=1000, blank=True, default='')
    creation_date = models.DateTimeField(_(u'Дата создания'), default=timezone.now)
    is_anonymous = models.BooleanField(default=False)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    likes_count = models.IntegerField(_(u'Количество лайков'), default=0)
    likes = models.ManyToManyField(User, related_name="liked_comments", through="CommentLike")

    is_active = models.BooleanField(default=True)
    spam_count = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return "Comment #" + str(self.id) + " by " + self.author.uid

    @staticmethod
    def comment_handler(sender, **kwargs):
        from push_service.models import NotificationHistory
        from push_service.tasks.comment_notification import comment_notification
        comment = kwargs.get('instance')
        question = comment.question
        user = question.author
        new_comment_history = NotificationHistory.objects.filter(user_id=user.id, entity='comment', action='new')
        recent_history = NotificationHistory.objects.filter(user_id=user.id,
                                                            date_created__gt=timezone.now() - timedelta(minutes=30))

        if not new_comment_history and user != comment.author:
            if not recent_history:
                comment_notification.apply_async((user.id, question.id, comment.id),)
            else:
                comment_notification.apply_async((user.id, question.id, comment.id),
                                                 eta=timezone.now() + timedelta(minutes=30))

class CommentLike(models.Model):
    class Meta:
        verbose_name = _(u'Лайк комментария')
        verbose_name_plural = _(u'Лайки комментариев')
        db_table = "d_comment_likes"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(_(u'Дата создания'), default=timezone.now)

    def __unicode__(self):
        return "Like for comment #" + str(self.comment.id) + \
               ", question #" + str(self.question.id) + " by " + self.user.uid

    @staticmethod
    def comment_like_handler(sender, **kwargs):
        from push_service.models import NotificationHistory
        from push_service.tasks.comment_notification import comment_like_notification

        comment_like = kwargs.get('instance')
        liker = comment_like.user
        comment = comment_like.comment
        author = comment.author
        question = comment.question
        comment_like_history = NotificationHistory.objects.filter(user_id=author.id, entity='comment', action='like')
        recent_history = NotificationHistory.objects.filter(user_id=author.id,
                                                            date_created__gt=timezone.now() - timedelta(minutes=30))

        if not comment_like_history and liker != author:
            if not recent_history:
                comment_like_notification.apply_async((author.id, question.id, comment.id),)
            else:
                comment_like_notification.apply_async((author.id, question.id, comment.id),
                                                        eta=timezone.now() + timedelta(minutes=30))


class Poll(models.Model):
    class Meta:
        verbose_name = _(u'Голосовалка')
        verbose_name_plural = _(u'Голосовалки')
        db_table = "d_poll"

    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    items_count = models.SmallIntegerField(_(u'Количество вариантов'), default=0)

    def __unicode__(self):
        return "Poll for question #" + str(self.question.id)


class PollItem(models.Model):
    class Meta:
        verbose_name = _(u'Вариант голосовалки')
        verbose_name_plural = _(u'Варианты голосовалок')
        db_table = "d_poll_item"

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(_(u'Текст варианта'), max_length=255, blank=True, default='')
    votes_count = models.SmallIntegerField(_(u'Количество голосов'), default=0)
    votes = models.ManyToManyField(User, related_name="voted_poll_items", through="Vote")
    picture = models.OneToOneField(Picture, blank=True, null=True)

    def __unicode__(self):
        return "Poll item for poll #" + str(self.poll.id) + " for question #" + str(self.question.id)


class Vote(models.Model):
    class Meta:
        verbose_name = _(u'Голос')
        verbose_name_plural = _(u'Голоса')
        db_table = "d_vote"
        unique_together = ('user', 'poll')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll_item = models.ForeignKey(PollItem, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(_(u'Дата создания'), default=timezone.now)

    def __unicode__(self):
        return "Vote for poll item #" + str(self.poll_item.id) + \
               " for poll #" + str(self.poll.id) + " by user " + str(self.user.uid)

    @staticmethod
    def vote_handler(sender, **kwargs):
        from push_service.models import NotificationHistory
        from push_service.tasks.vote_notification import vote_notification

        vote = kwargs.get('instance')
        voter = vote.user
        question = vote.poll.question
        author = question.author

        vote_history = NotificationHistory.objects.filter(user_id=author.id, entity='question', action='vote')
        recent_history = NotificationHistory.objects.filter(user_id=author.id,
                                                            date_created__gt=timezone.now() - timedelta(minutes=30))

        if not vote_history and voter != author:
            if not recent_history:
                vote_notification.apply_async((author.id, question.id),)
            else:
                vote_notification.apply_async((author.id, question.id),
                                              eta=timezone.now() + timedelta(minutes=30))


class Locale(models.Model):
    class Meta:
        verbose_name = _(u'Локаль')
        verbose_name_plural = _(u'Локали')
        ordering = ('name', )
        db_table = "d_locale"

    name = models.CharField(max_length=10, verbose_name=u'Название')
    categories = models.ManyToManyField(Category, related_name="locales", through="LocaleCategory")

    def __unicode__(self):
        return self.name


class LocaleCategory(models.Model):
    class Meta:
        verbose_name = _(u'Локаль категории')
        verbose_name_plural = _(u'Локали категорий')
        db_table = "d_locale_category"

    locale = models.ForeignKey(Locale, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u'Название')

    def __unicode__(self):
        return "Locale " + self.locale.name + " for category " + str(self.category.id)


class SpamReport(models.Model):
    class Meta:
        verbose_name = _(u'Пометка о спаме')
        verbose_name_plural = _(u'Пометки о спаме')
        db_table = "d_spam_report"

    ENTITIES = (('question', 'question'),
                ('comment', 'comment'))

    entity = models.CharField(max_length=255, choices=ENTITIES)
    entity_id = models.PositiveIntegerField()
    user = models.ForeignKey(User)


post_save.connect(Comment.comment_handler, sender=Comment)
post_save.connect(CommentLike.comment_like_handler, sender=CommentLike)
post_save.connect(Vote.vote_handler, sender=Vote)
