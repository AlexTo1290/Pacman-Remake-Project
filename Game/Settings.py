class Settings:
    """Contains the settings of the game. Static variables can be adjusted to change the game."""
    WINDOW_WIDTH = 1600
    WINDOW_HEIGHT = 900
    GAME_SPEED = 30
    PACMAN_MOVE_LENGTH = 5
    GHOST_MOVE_LENGTH = 5
    SCORE_INCREASE_ON_COIN = 10
    SCORE_INCREASE_ON_WIN = 500

    # Probably of each ghost calculating its direct path to the player (per game tick)
    INKY_PATH_FIND_PROB = 0
    PINKY_PATH_FIND_PROB = 0
    BLINKY_PATH_FIND_PROB = 0
    CLYDE_PATH_FIND_PROB = 0