from data_insertion import *
from db_connection import connect_to_database_mysql
from img_insertion import fetch_img_from_api


def main():
    """Main function to handle the database migration."""
    db = connect_to_database_mysql()
    if db is None:
        print("Failed to connect to the database.")
        return

    cursor = db.cursor()
    data = read_json()

    insert_pokemons(cursor, data)
    insert_types(cursor, data)
    insert_trainers(cursor, data)
    insert_pokemon_types(cursor, data)
    insert_teams(cursor, data)

    db.commit()
    cursor.close()
    db.close()



if __name__ == "__main__":
    main()
