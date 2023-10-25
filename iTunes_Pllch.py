#########################################
##### Name: Paul Lellouche          #####
##### Uniqname: pllch               #####
#########################################

import json as JSON
import requests
import webbrowser


class Media:

    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", json=None):

        if json is not None: #JSON.loads(json) prior to this step?

            if json["wrapperType"] == "track":
                self.title = json["trackName"]
                self.url = json["trackViewUrl"]

            else:
                self.title = json["collectionName"]
                self.url = json["collectionViewUrl"]

            self.author = json["artistName"]
            self.release_year = json["releaseDate"][0:4] #convert to int?

        else:
            self.title = title
            self.author = author
            self.release_year = release_year
            self.url = url

    def info(self):
        return f"{self.title} by {self.author} ({self.release_year})" #fstring or concatenation

    def length(self):
        return 0



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


def searchItunes(query, limit = 5): #define input() elsewhere

    base_url = "https://itunes.apple.com/search"
    params = {
        "term": query,
        "limit": limit
    }

    response = requests.get(base_url, params=params)
    query_result = response.json() # check returns as dict

    return query_result


def obj_list(query_result, result_list=[]):


    for i in query_result["results"]:
        if i["wrapperType"] == "track":

            if i["kind"] == "song":
                result_list.append(Song(json=i))
            else:
                result_list.append(Movie(json=i))

        else:
            result_list.append(Media(json=i))

    return result_list


def obj_type(result_list):

    song_list = []
    movie_list = []
    media_list = []

    for i in result_list:

        if type(i) == Song:
            song_list.append(i)

        elif type(i) == Movie:
            movie_list.append(i)

        else:
            media_list.append(i)

    return song_list, movie_list, media_list




if __name__ == "__main__":
    # your control code for Part 4 (interactive search) should go here



    #take input


    #while input not exit,
    while True:
        usr_input = input('Enter a search term, or "exit" to quit: ') #if moved within while true it would have updated

        if usr_input != "exit":
            query = usr_input

            query_result = searchItunes(query, limit=5)


            result_list = obj_list(query_result)
            song_list, movie_list, media_list = obj_type(result_list)
            ordered_list = []

            print(f"\nSONGS\n")
            for i, song in enumerate(song_list, 1):
                print(f"{i}. {song.info()}")
                ordered_list.append(song)
                numsave = i

            print(f"\nMOVIES\n")
            for i, movie in enumerate(movie_list, 1):
                print(f"{i+numsave}. {movie.info()}")
                ordered_list.append(movie)
                numsave = numsave + i

            print(f"\nOTHER MEDIA\n")
            for i, media in enumerate(media_list, 1):
                print(f"{i+numsave}. {media.info()}")
                ordered_list.append(media)

            while True: #Alternative to using break - set variable to true, then change if exit

                second_input = input("Enter a number for more info, or another search term, or exit: ")

                if second_input == "exit":
                    print("Bye!")
                    break #Will break out of master loop?

                else:

                    try:
                        second_input = int(second_input)

                        if 1 <=  second_input <= len(result_list):
                            tv_url = ordered_list[second_input-1].url
                            print(f"Launching\n{tv_url}\nin web browser...")
                            webbrowser.open(tv_url)

                        else:
                            print("Invalid input, number out of range")

                    except ValueError:
                        break


            usr_input = second_input


        else:
            print("Bye!")
            break




    #Call search itunes
    #Call obj_list
    #Call obj_type
    #Loop through songlist first, have counter, print counter then Song.info()
    #Then movielist start counter at len(song_list)
    #Then medialist start counter at len(song_list) + len (media_list)
    #Prompt for number, search term, or exit
        #exit breaks loop - output bye
        #If number outside of 1 - len(song_list)+len(media_list)+len(movie_list)
            ##Prompt for number, search term, or exit
        #If number between 1 and len(song_list)
            #launch https://itunes.apple.com/search/us/song_list[number].name()
        #If number between len(song_list) and len(movie_list) + len(song_list)
            #launch https://itunes.apple.com/search/us/movie_list[number-len(song_list)].name()
        #If number between len(movie_list) +len(song_list) and len(song_list)+len(media_list)+len(movie_list)
            #launch https://itunes.apple.com/us/movie_list[number-len(song_list)-len(movie_list)].name()

