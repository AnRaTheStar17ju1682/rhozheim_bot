class PlaylistNotAllowedError(Exception):
    """Исключение возникает при попытке загрузки плейлиста"""
    def __init__(self, message="Downloading playlists is not allowed"):
        self.message = message
        super().__init__(self.message)