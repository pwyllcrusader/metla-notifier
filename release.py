class Release:
    def __init__(
        self,
        cover_link,
        artist,
        album,
        year,
        genre,
        country,
        file,
        size,
        download_links,
    ):
        self.cover_link = cover_link
        self.artist = artist
        self.album = album
        self.year = year
        self.genre = genre
        self.country = country
        self.file = file
        self.size = size
        self.download_links = download_links

    def __str__(self):
        # TODO implement it right
        return f"""             #image
                    *Arist*: {self.artist}
                    *Album*: {self.album}
                    *Year*: {self.year}
                    *Genre*: {self.genre}
                    *Country*: {self.country}
                    *File*: {self.file}
                    *Size*: {self.size}
                    *Links*: {' '.join(self.get_file_links())}
        """

    def get_file_links(self):
        return [f"[link]({link})" for link in self.download_links]
