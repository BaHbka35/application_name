from django.contrib import admin

from .models import Challenge, ChallengeMember, ChallegeWinner, ChallengeAnswer

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    """Setting for challenge admin page."""

    list_display = ('name', 'creator', 'finish_datetime',
                    'bet', 'total_bets_sum',)
    readonly_fields = ('start_datetime', 'total_bets_sum',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('creator', 'bet',)
    search_fields = ('name', 'creator__username',)


@admin.register(ChallengeMember)
class ChallengeMemberAdmin(admin.ModelAdmin):
    """Setting for challenge member admin page."""
    list_display = ('user', 'challenge',)


@admin.register(ChallegeWinner)
class ChallengeWinnerAdmin(admin.ModelAdmin):
    """Setting for challenge winner admin page."""
    list_display = ('challenge_member', 'challenge',)


@admin.register(ChallengeAnswer)
class ChallengeAnserAdmin(admin.ModelAdmin):
    """Setting for challenge answer admin page."""
    list_display = ('challenge_member', 'challenge',)
