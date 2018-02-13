There should be four files in the folder including this readme file. Really
only the exe file is needed to get the app up and running. 

-filmsack.exe
-filmsack.db
-filmsack.csv
-readme.txt

The exe file actually downloads the csv file from imdb.com and stores it 
locally. Next, it prompts the user for the stat they wish to display. 

    Welcome to the
    _____________________________________________________________________
     _____   _   _           ___  ___   _____       ___   _____   _   _
    |  ___| | | | |         /   |/   | /  ___/     /   | /  ___| | | / /
    | |__   | | | |        / /|   /| | | |___     / /| | | |     | |/ /
    |  __|  | | | |       / / |__/ | | \___  \   / / | | | |     | |\ \
    | |     | | | |___   / /       | |  ___| |  / /  | | | |___  | | \ \
    |_|     |_| |_____| /_/        |_| /_____/ /_/   |_| \_____| |_|  \_\
    ---------------------------------------------------------------------
                                                            Top Sacked App


    Enter a selection:
        "1" - Actors
        "2" - Directors
        "3" - Producers
        "4" - Writers
        "5" - Composers
        "6" - Years
        "rebuild" - Rebuild Database
    >

The rebuild option is only needed if there is no database file for it to
read from or there have been more movies added to the show list on imdb. If 
the user chooses this option they are then warned of the time it takes and 
asked to comfirm the rebuild. 

    Rebuilding the database will take some time. Once started, it will need to 
    complete before you are able to use the program again. Continue? y/n:
    >

Choosing one of the stats to display will be followed with a prompt asking
for the least number of times that the given cast/crew appears in the list
of movies. 

In the following example we chose to display the actors that appeared in 4
or more movies in our list.

    Enter the least number of times the actor has appeared:
    > 4
    Actors featured in 4 or more films
    ==================================
    James Remar......................5
    Majel Barrett....................5
    Bradley Lavelle..................4
    Eugene Lipinski..................4
    Jared Chandler...................4
    Samuel L. Jackson................4
    Steve Buscemi....................4
    William Shatner..................4

If you choose a number higher than any stat (in the case above, actor) then 
an empty list is returned. Restart the app and choose a lower value. 

enjoy.