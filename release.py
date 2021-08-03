class Release:
    pict_link = ""
    artist = ""
    album = ""
    year = ""
    genre = ""
    country = ""
    file = ""
    size = ""
    download_links = []

    def __init__(
        self,
        pict_link,
        artist,
        albun,
        year,
        genre,
        country,
        file,
        size,
        download_links
    ):
        self.pict_link = pict_link
        self.artist = artist
        self.album = albun
        self.year = year
        self.genre = genre
        self.country = country
        self.file = file
        self.size = size
        self.download_links = download_links

    def __str__(self):
        # TODO implement it
        ...
