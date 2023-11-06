from build_game import start_game
from database_actions import set_default_values, inicjalize_db

if __name__ == "__main__":
    inicjalize_db()
    set_default_values()
    start_game() 