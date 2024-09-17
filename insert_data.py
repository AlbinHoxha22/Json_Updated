from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from db_schema import Base, Nationality, Championship, Player, Match, Trophy
from utils import transform_data, find_highest_scoring_match, count_player_trophies

# Create an SQLite database
engine = create_engine("sqlite:///snooker.db")
Base.metadata.create_all(engine)  # Ensure tables are created

Session = sessionmaker(bind=engine)
session = Session()


def insert_data(transformed_data):
    # Insert nationalities
    for nationality_data in transformed_data["nationalities"]:
        nationality = Nationality(**nationality_data)
        session.add(nationality)

    # Insert championships
    for championship_data in transformed_data["championships"]:
        championship = Championship(**championship_data)
        session.add(championship)

    # Insert players, matches, and trophies
    for player_data in transformed_data["players"]:
        player = Player(
            first_name=player_data["first_name"],
            last_name=player_data["last_name"],
            nationality_id=player_data["nationality_id"],
        )
        session.add(player)
        session.flush()  # Get player.id after insertion

        # Insert matches for each player
        for match_data in transformed_data["matches"]:
            if match_data["player_id"] == player.id:
                match = Match(
                    championship_id=match_data["championship_id"],
                    player=player,
                    frames_won=match_data["frames_won"],
                    frames_lost=match_data["frames_lost"],
                    total_points=match_data["total_points"],
                )
                session.add(match)

        # Insert trophies for each player
        for trophy_data in transformed_data["trophies"]:
            if trophy_data["player_id"] == player.id:
                trophy = Trophy(
                    name=trophy_data["name"], year=trophy_data["year"], player=player
                )
                session.add(trophy)

        # Commit after matches and trophies are inserted
        session.flush()

        # Find highest scoring match and number of trophies
        highest_scoring_match_id = find_highest_scoring_match(
            transformed_data, player.id
        )
        trophies_won = count_player_trophies(transformed_data, player.id)

        # Update the player with highest scoring match and trophies won
        player.highest_scoring_match_id = highest_scoring_match_id
        player.trophies_won = trophies_won

    # Commit the session
    session.commit()
    session.close()


if __name__ == "__main__":
    # Load JSON data
    with open("seed.json", "r") as file:
        data = json.load(file)

    # Transform the data
    transformed_data = transform_data(data)

    # Insert data into the database
    insert_data(transformed_data)
