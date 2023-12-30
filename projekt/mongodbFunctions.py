from pymongo import MongoClient


def insert_team_mongodb(team_name, team_id):
    # Establish a connection to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client.projekt  # Replace 'your_database' with your actual database name
    players_collection = db.team_player  # Replace 'players' with your actual collection name

    # Create a document to insert
    team_document = {
        "_id": team_id,
        "team_name": team_name
    }

    # Insert the document into the collection
    players_collection.insert_one(team_document)

    # Close the MongoDB connection
    client.close()


def insert_player_mongodb(team_id, player_name, player_id):
    client = MongoClient('mongodb://localhost:27017/')
    db = client.projekt  # Replace 'your_database' with your actual database name
    team_player_collection = db.team_player  # Replace 'players' with your actual collection name

    # Update the document in the collection
    query = {"_id": team_id}
    update_query = {"$push":
        {"players":
            {
                "player_id": player_id,
                "player_name": player_name
            }
        }
    }
    team_player_collection.update_one(query, update_query)

    # Close the MongoDB connection
    client.close()
