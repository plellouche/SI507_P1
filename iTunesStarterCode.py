#########################################
##### Name: Paul Lellouche          #####
##### Uniqname: pllch               #####
#########################################

import json as JSON


class Media:

    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", json=None):

        if json is not None:

            if json["WrapperType"] == "track":
                self.title = json["trackName"]
                self.url = json["trackViewUrl"]

            else:
                self.title = json["collectionName"]
                self.url = json["collectionViewUrl"]

            self.author = json["artistName"]
            self.release_year = json["releaseDate"][0:3] #convert to int?

        else:
            self.title = title
            self.author = author
            self.release_year = release_year
            self.url = url

    def info(self):
        return f"{self.title} by {self.author} ({self.release_year})" #fstring or concatenation

    def length(self):
        return 0



# Other classes, functions, etc. should go here

class Song(Media): #Where use super for subclasses?

    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", album="No Album", genre="No Genre", track_length=0, json=None):
        super().__init__(title, author, release_year, url, json)

        if json is not None:

            if json["kind"] == "song": #only include song types?
                self.track_length = json["trackTimeMillis"]
                self.album = json["collectionName"]
                self.genre = json["primaryGenreName"]

            else:
                self.track_length = None
                self.album = None
                self.genre = None

        else:

            self.album = album
            self.genre = genre
            self.track_length = track_length


    def info(self):
        return super().info() + f" [{self.genre}]"


    def length(self):
        return round(self.track_length/1000) #may need to use datetime class here



class Movie(Media):

    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", rating="No Rating", movie_length=0, json=None):
        super().__init__(title, author, release_year, url, json)

        if json is not None:

            if json["kind"] == "feature-movie":
                self.rating = json["contentAdvisoryRating"]
                self.movie_length = json["trackTimeMillis"]

            else:
                self.rating = None
                self.movie_length = None

        else:
            self.rating = rating
            self.movie_length = movie_length

    def info(self):
        return super().info() + f" [{self.rating}]"

    def length(self):
        return round((self.movie_length/60000)) #may need to use datetime class here


if __name__ == "__main__":
    # your control code for Part 4 (interactive search) should go here
    pass
