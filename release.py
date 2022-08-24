class Release:
    def __init__(
        self,
        topic,
        cover_link,
        artist,
        album,
        year,
        genre,
        country,
        file,
        size,
        download_links,
        uploaded_at
    ):
        self.topic = topic
        self.cover_link = cover_link
        self.artist = artist.replace(":", "").strip()
        self.album = album.replace(":", "").strip()
        self.year = year.replace(":", "").strip()
        self.genre = genre.replace(":", "").strip()
        self.country = country.replace(":", "").strip()
        self.file = file.replace(":", "").strip()
        self.size = size.replace(":", "").strip()
        self.download_links = download_links
        self.uploaded_at = uploaded_at

    def __str__(self):
        return f"""[ ]({self.cover_link})
*Arist*: {self.artist}
*Album*: {self.album}
*Year*: {self.year}
*Genre*: {self.genre}
*Country*: {self.country}
*File*: {self.file}
*Size*: {self.size}
*Links*: [topic]({self.topic}) {' '.join(self.get_file_links())}"""

    def get_file_links(self):
        return [f"[link]({link})" for link in self.download_links]
