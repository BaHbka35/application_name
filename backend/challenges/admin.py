from django.contrib import admin

from .models import Challenge, ChallengeMember, ChallegeWinner, ChallengeAnswer

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    """Setting for challenge admin page."""

    list_display = ('name', 'creator', 'date_finish', 'bet', 'total_bets_sum',)
    readonly_fields = ('date_start', 'total_bets_sum',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('creator', 'bet',)
    search_fields = ('name', 'creator__username',)


@admin.register(ChallengeMember)
class ChallengeAdmin(admin.ModelAdmin):
    """Setting for challenge member admin page."""
    pass


@admin.register(ChallegeWinner)
class ChallengeAdmin(admin.ModelAdmin):
    """Setting for challenge winner admin page."""
    pass


@admin.register(ChallengeAnswer)
class ChallengeAdmin(admin.ModelAdmin):
    """Setting for challenge answer admin page."""
    pass
