import requests
import sqlite3
import csv
from bs4 import BeautifulSoup
from imdbpie import Imdb
imdb = Imdb()

# creates/connects to our database 
conn = sqlite3.connect('filmsack.db')
c = conn.cursor()


url = 'http://www.imdb.com/list/ls021979042/export?ref_=ttls_exp'
r = requests.get(url)

with open('filmsack.csv', 'wb') as f:
    f.write(r.content)

# title header for app. print statements ftw!
def ascii_title():
    print()
    print('Welcome to the')
    print('_' * 69)
    print(' _____   _   _           ___  ___   _____       ___   _____   _   _  ')
    print('|  ___| | | | |         /   |/   | /  ___/     /   | /  ___| | | / /  ')
    print('| |__   | | | |        / /|   /| | | |___     / /| | | |     | |/ /   ')
    print('|  __|  | | | |       / / |__/ | | \___  \   / / | | | |     | |\ \   ')
    print('| |     | | | |___   / /       | |  ___| |  / /  | | | |___  | | \ \  ')
    print('|_|     |_| |_____| /_/        |_| /_____/ /_/   |_| \_____| |_|  \_\ ')
    print('-' * 69)
    print('                                                       Top Sacked App')
    print()
    print()


# drop and create tables functions for the database
def create_tables():
    c.execute('''CREATE TABLE IF NOT EXISTS titleAndID(movieID TEXT,
                movieTitle TEXT, movieYear TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS movieStars(movieID TEXT, 
                actor TEXT, role TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS movieDirectors(movieID TEXT, 
                director TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS movieComposers(movieID TEXT, 
                composer TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS movieWriters(movieID TEXT, 
                writer TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS movieProducers(movieID TEXT,
                producer TEXT)''')
    conn.commit()


def build_db():
    c.execute('DROP TABLE IF EXISTS titleAndID')
    c.execute('DROP TABLE IF EXISTS movieStars')
    c.execute('DROP TABLE IF EXISTS movieDirectors')
    c.execute('DROP TABLE IF EXISTS movieComposers')
    c.execute('DROP TABLE IF EXISTS movieWriters')
    c.execute('DROP TABLE IF EXISTS movieProducers')
    create_tables()


def parseMovieStats(x):
    movieCredits = {}
    print('Getting cast for ' + str(len(x)) + ' movies....')
    counter = len(x)
    for id in x:
        title = list(c.execute('SELECT * FROM titleAndID WHERE movieID = ' + "'" + id + "'"))[0]
        print(str(counter) + ') ' + title[2] + ' - ' + title[1])
        counter -= 1
        movieCredits = imdb.get_title_credits(id)['credits']
        for star in movieCredits['cast']:
            actor = str(star['name'])
            try:
                role = str(star['characters'])
            except Exception as e:
                role = '  Not listed  '
            #print(id, actor, role[2:-2])
            c.execute('''INSERT INTO movieStars (movieID, actor, role)
                    VALUES (?, ?, ?)''', (id, actor, role))
            conn.commit() 

        
        for star in movieCredits['director']:
            dir = str(star['name'])
            #print(dir)
            c.execute('''INSERT INTO movieDirectors (movieID, director)
                    VALUES (?, ?)''', (id, dir))
            conn.commit()

        
        try:
            for star in movieCredits['writer']:
                write = str(star['name'])
        except Exception as e:
            write = 'Not listed'
        #print(write)
        c.execute('''INSERT INTO movieWriters (movieID, writer)
                    VALUES (?, ?)''', (id, write))
        conn.commit()

        
        try:
            for star in movieCredits['composer']:
                comp = str(star['name'])
        except Exception as e:
            comp = 'Not listed'
        #print(comp)
        c.execute('''INSERT INTO movieComposers (movieID, composer)
                    VALUES (?, ?)''', (id, comp))
        conn.commit()

        
        try:
            for star in movieCredits['producer']:
                prod = str(star['name'])
        except Exception as e:
            prod = 'Not listed'
        #print(prod)
        c.execute('''INSERT INTO movieProducers (movieID, producer)
                    VALUES (?, ?)''', (id, prod))
        conn.commit()


def read_movieIDs():
    c.execute('SELECT * FROM titleAndID')
    ids = []
    for row in c.fetchall():
        ids.append(row[0])
    return ids

# reads the csv file downloaded from IMDB list.
def parse_movie_list():
    with open('Filmsack.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        #next(csv_reader)
        for line in csv_reader:
            idNum = line['Const']
            idName = line['Title']
            idYear = line['Year']
            c.execute('''INSERT INTO titleAndID (movieID, movieTitle,
                      movieYear) VALUES (?, ?, ?)''', (idNum, idName, idYear))
            conn.commit()


# defs that output the counts for the various info parsed above
def top_directors(z):
    print('Directors featured in ' + z +' or more films')
    print('=' * 37)
    for row in c.execute('''SELECT director, COUNT(director) FROM movieDirectors
                         GROUP BY director HAVING count(*) >= ''' + z +
                         ' ORDER BY COUNT(director) desc'):
        print(list(row)[0].ljust(20, ".") + str(list(row)[1]))
    print()


def top_years(z):
    print('Years that ' + z +' or more movies were sacked')
    print('=' * 41)
    for row in c.execute('''SELECT movieYear, COUNT(movieYear) FROM titleAndID
                         GROUP BY movieYear HAVING count(*) >= ''' + z +
                         ' ORDER BY COUNT(movieYear) desc'):
        print(list(row)[0].ljust(5, "-") + str(list(row)[1]))
    print()


def top_actors(z):
    print('Actors featured in ' + z +' or more films')
    print('=' * 34)
    for row in c.execute('''SELECT actor, COUNT(actor) FROM movieStars
                         GROUP BY actor HAVING count(*) >= ''' + z +
                         ' ORDER BY COUNT(actor) desc'):
        print(list(row)[0].ljust(32, ".") + str(list(row)[1]).rjust(2, "."))
    print()


def top_producers(z):
    print('Producers featured in ' + z +' or more films')
    print('=' * 37)
    for row in c.execute('''SELECT producer, COUNT(producer) FROM movieProducers
                         GROUP BY producer HAVING count(*) >= ''' + z +
                         ' ORDER BY COUNT(producer) desc'):
        print(list(row)[0].ljust(35, ".") + str(list(row)[1]).rjust(2, "."))
    print()


def top_writers(z):
    print('Writers featured in ' + z +' or more films')
    print('=' * 35)
    for row in c.execute('''SELECT writer, COUNT(writer) FROM movieWriters
                         GROUP BY writer HAVING count(*) >= ''' + z +
                         ' ORDER BY COUNT(writer) desc'):
        print(list(row)[0].ljust(31, ".") + str(list(row)[1]).rjust(2, "."))
    print()


def top_composers(z):
    print('Composers featured in ' + z +' or more films')
    print('=' * 37)
    for row in c.execute('''SELECT composer, COUNT(composer) FROM movieComposers
                         GROUP BY composer HAVING count(*) >= ''' + z +
                         ' ORDER BY COUNT(composer) desc'):
        print(list(row)[0].ljust(35, ".") + str(list(row)[1]).rjust(2, "."))
    print()


ascii_title()



print('''Enter a selection: 
    "1" - Actors
    "2" - Directors
    "3" - Producers
    "4" - Writers
    "5" - Composers
    "6" - Years
    "rebuild" - Rebuild Database''')
while True:
    a = input("> ")
    if a == '1':
        print('Enter the least number of times the actor has appeared:')
        print('A number too high will result in an empty list.')
        times = input('> ')
        top_actors(times)
        break
    if a == '2':
        print('Enter the least number of times the director has appeared:')
        print('A number too high will result in an empty list.')
        times = input('> ')
        top_directors(times)
        break
    if a == '3':
        print('Enter the least number of times the producer has appeared:')
        print('A number too high will result in an empty list.')
        times = input('> ')
        top_producers(times)
        break
    if a == '4':
        print('Enter the least number of times the writer has appeared:')
        print('A number too high will result in an empty list.')
        times = input('> ')
        top_writers(times)
        break
    if a == '5':
        print('Enter the least number of times the composer has appeared:')
        print('A number too high will result in an empty list.')
        times = input('> ')
        top_composers(times)
        break
    if a == '6':
        print('Enter the least number of times the year has appeared:')
        print('A number too high will result in an empty list.')
        times = input('> ')
        top_years(times)
        break
    if a.lower() == 'rebuild':
        print('''Rebuilding the database will take some time.\
                Once started, it will need to complete before you\
                are able to use the program again. Continue? y/n: ''')
        refresh = input('> ')
        if refresh.lower() == 'y':
            print('Standby while we build the database... ')
            build_db()
            parse_movie_list()
            ids = read_movieIDs()
            parseMovieStats(ids)
            print('Database has been built, this only has to be done again when new\
            movies are added.')
        else:
            pass
        break
    print('Need to pick 1 through 6, not whatever you entered... try again')

#        print(line['Const'], line['Title'].ljust(35), line['Directors'])
# http://www.imdb.com/list/ls021979042/export?ref_=ttls_exp

print()
print()
input('Press Enter to close... ')

c.close()
conn.close()
