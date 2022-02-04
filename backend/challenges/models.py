from django.db import models

from users.models import User


class Challenge(models.Model):
    """Challenge model"""

    name = models.CharField(max_length=200, verbose_name='challenge name')

    slug = models.SlugField(max_length=200, unique=True, verbose_name='slug')

    creator = models.ForeignKey(User, on_delete=models.CASCADE,
                                verbose_name='challenge creator')

    start_datetime = models.DateTimeField(
        auto_now_add=True, verbose_name='date when challenge starts')

    finish_datetime = models.DateTimeField(
        verbose_name='date when challenge finishes')

    goal = models.CharField(max_length=200, verbose_name='what must be done')

    description = models.CharField(max_length=500,
                                   verbose_name='challenge discription')

    requirements = models.CharField(
        verbose_name='requirements for how challenge must be done',
        max_length=500)

    video_example = models.FileField(upload_to='video_examples',
                                     verbose_name='example of perform',
                                     blank=True, null=True)

    bet = models.PositiveIntegerField(
        default=0, verbose_name='amount coins for accept challenge')

    total_bets_sum = models.PositiveIntegerField(
        verbose_name='total sum of all bets for this challenge', default=0)

    is_active = models.BooleanField(verbose_name='is challenge active',
                                    default=True)

    def __str__(self):
        return self.name


class ChallengeMember(models.Model):
    """User that accept challenge."""

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='user')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE,
                                  verbose_name='challenge')

    def __str__(self):
        return self.user.username


class ChallegeWinner(models.Model):
    """User that wone challenge."""

    challenge_member = models.ForeignKey(
        ChallengeMember, on_delete=models.CASCADE,
        verbose_name='challenge member')

    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE,
                                  verbose_name='challenge')

    def __str__(self):
        return f'winner "{self.challenge_member.user.username}" \
            of challenge "{self.challenge.name}"'


class ChallengeAnswer(models.Model):
    """Video answer on challenge."""

    challenge_member = models.ForeignKey(
        ChallengeMember, on_delete=models.CASCADE,
        verbose_name='challenge member')

    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE,
                                  verbose_name='challenge')

    video_answer = models.FileField(upload_to='video_answer',
                                    verbose_name='video answer on chellange',)

    def __str__(self):
        return f'asnwer from "{self.challenge_member.user.username}" \
            for challenge "{self.challenge.name}"'
