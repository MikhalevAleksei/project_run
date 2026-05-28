from geopy.distance import geodesic

from app_run.models import Position


def calculate_run_distance(run):
    positions = Position.objects.filter(run=run).order_by('created_at')

    total_distance = 0
    previous_position = None

    for position in positions:
        if previous_position is not None:
            previous_point = (
                previous_position.latitude,
                previous_position.longitude,
            )

            current_point = (
                position.latitude,
                position.longitude,
            )

            total_distance += geodesic(previous_point, current_point).kilometers

        previous_position = position

    return round(total_distance, 3)