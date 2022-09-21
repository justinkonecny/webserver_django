t_track = dict[str, str | int]


def get_tracks_from_query(query_results, filter_dupes=True, limit=50) -> list[t_track]:
    tracks = [{
        "created_at": track_rec.created_at,
        "from_username": track_rec.user_from.username,
        "to_username": track_rec.user_to.username,
        "spotify_track_id": track_rec.spotify_track_id,
        "has_listened": track_rec.has_listened,
    } for track_rec in query_results[:limit]]
    return filter_duplicates(tracks) if filter_dupes else tracks


def filter_duplicates(tracks: list[t_track]) -> list[t_track]:
    unique = tracks[:1]
    for track in tracks[1:]:
        last_track = unique[-1]
        if track["spotify_track_id"] != last_track["spotify_track_id"]:
            unique.append(track)
    return unique
