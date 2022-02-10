from django.contrib import admin

from .models import Challenge, ChallengeMember, ChallegeWinner,\
                    ChallengeAnswer, ChallengeBalance

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    """Setting for challenge admin page."""

    list_display = ('name', 'creator', 'finish_datetime', 'bet')
    readonly_fields = ('start_datetime', 'id')
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


@admin.register(ChallengeBalance)
class ChallengeBalanceAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'coins_amount',)
