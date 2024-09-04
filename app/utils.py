import csv

from datetime import datetime
from django.db import transaction
from django.http import HttpResponse

from models_2 import PlayerLevel, LevelPrize, Prize


def assign_prize_to_player(player_id, level_id, prize_id):
    with transaction.atomic():
        player_level = PlayerLevel.objects.get(player_id=player_id, level_id=level_id)
        prize = Prize.objects.get(id=prize_id)

        LevelPrize.objects.create(level=player_level.level, prize=prize, received=datetime.now())
        player_level.is_completed = True
        player_level.save()


def export_player_data_to_csv():
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="player_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Player ID', 'Level Title', 'Is Completed', 'Prize Title'])

    player_levels = PlayerLevel.objects.select_related('player', 'level').iterator()

    for player_level in player_levels:
        level_prizes = LevelPrize.objects.filter(level=player_level.level)
        for level_prize in level_prizes:
            writer.writerow([
                player_level.player.player_id,
                player_level.level.title,
                player_level.is_completed,
                level_prize.prize.title
            ])

    return response
