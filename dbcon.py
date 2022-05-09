import psycopg2

conn = psycopg2.connect(dbname='moviebotdb', user='postgres', password='rookie')  # local test connection


# conn = psycopg2.connect(dbname='postgres', user='root', password='root')          # public server connection


def db_load(action, db_name, entity, *option):
    with conn.cursor() as cur:
        db_variations = {"movies": "(title, watched)",
                         "quotes": "(text, movie_title, timestamp)"}
        db_options = {"not_watched": "WHERE watched=false"}
        if option == ():
            option = ""
        else:
            option = db_options[option[0]]

        db_commands = {"insert": f"INSERT INTO {db_name} {db_variations[db_name]} VALUES {entity}",
                       "select": f"SELECT {entity} FROM {db_name} {option}",
                       "delete": f"DELETE FROM {db_name} WHERE {'title' if db_name == 'movies' else 'text'}='{entity}'",
                       "update": f"UPDATE {db_name} SET watched=true WHERE title='{entity}'"}

        cur.execute(db_commands[action] + ";")
        if action != "select":
            conn.commit()
            return cur.statusmessage
        elif action == "select":
            return cur.fetchall()

