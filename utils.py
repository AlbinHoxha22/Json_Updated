def transform_data(data):
    transformed_data = {
        "nationalities": [],
        "championships": [],
        "players": [],
        "matches": [],
        "trophies": [],
    }

    # Transform nationalities
    transformed_data["nationalities"] = [
        {"id": nationality["id"], "name": nationality["name"]}
        for nationality in data.get("nationalities", [])
    ]

    # Transform championships
    transformed_data["championships"] = [
        {
            "id": champ["id"],
            "name": champ["name"],
            "nationality_id": champ["nationality_id"],
        }
        for champ in data.get("championships", [])
    ]

    # Transform players, matches, and trophies
    for player_data in data.get("players", []):
        player_id = player_data["id"]
        transformed_data["players"].append(
            {
                "id": player_id,
                "first_name": player_data["first_name"],
                "last_name": player_data["last_name"],
                "nationality_id": player_data["nationality_id"],
            }
        )

        # Transform matches
        for match_data in player_data.get("matches", []):
            transformed_data["matches"].append(
                {
                    "id": match_data["id"],
                    "championship_id": match_data["championship_id"],
                    "player_id": player_id,
                    "frames_won": match_data["frames_won"],
                    "frames_lost": match_data["frames_lost"],
                    "total_points": match_data["total_points"],
                }
            )

        # Transform trophies
        for trophy_data in player_data.get("trophies", []):
            transformed_data["trophies"].append(
                {
                    "id": trophy_data["id"],
                    "name": trophy_data["name"],
                    "year": trophy_data["year"],
                    "player_id": player_id,
                }
            )

    return transformed_data


def find_highest_scoring_match(transformed_data, player_id):
    """Find the match with the most points for a specific player and return its ID."""
    highest_points = 0
    highest_scoring_match_id = None
    for match in transformed_data["matches"]:
        if match["player_id"] == player_id and match["total_points"] > highest_points:
            highest_points = match["total_points"]
            highest_scoring_match_id = match["id"]

    return highest_scoring_match_id


def count_player_trophies(transformed_data, player_id):
    """Count the number of trophies a player has won."""
    return sum(
        1 for trophy in transformed_data["trophies"] if trophy["player_id"] == player_id
    )
