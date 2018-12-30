#! /usr/bin/python3
""" populate the movie database with csv file content """
#from models import Movie, Director
import sys
import csv

def catenate(s1,s2):
        s1=s1.strip()
        s2=s2.strip()
        if s1:
                if s2:
                        return s1+" "+s2
                else:
                        return s1
        else:
                return s2

movie_reader = csv.reader(open('data/Filmothèque.csv'), delimiter=";")
i=0
directors_count=0
directors={}
movies=[]

#
# one pass on input file to fill directors table and movies table
#
for movie_row in movie_reader:
        #
        # directors first
        # this line may pose a pb if fn1+ln1 == fn2+ln2
        fn=movie_row[0].strip()
        ln=movie_row[1].strip()
        director_key=" ".join([fn,ln])
        if director_key in directors:
                director_id=directors[director_key][0]
        else:
                directors_count+=1
                directors[director_key]=(directors_count, fn, ln)
                director_id=directors_count
        #
        # movies last
        # input file is assumed without duplicate lines
        # Same title with different duration, comment, is allowed
        #
        movie_director=director_id
        movie_title=movie_row[2]
        movie_comment = catenate(movie_row[3], movie_row[4])
        movies.append((movie_director, movie_title, movie_comment))
#
# sort directors in increasing id order
#
sd= sorted(directors.items(), key=lambda kv: kv[1][0])

#
# open output file
with open('fixtures/inidb.json','tw') as fo:
        #begin json list
        fo.write('[\n')
        # dump director table first
        model_name="moviedb.director"
        first=True
        for d in sd:
                #begin json item
                if first:
                        first=False
                else:
                        fo.write(",\n")
                fo.write("\t{\n")
                fo.write("\t\t\"model\": \""+ model_name+ "\",\n")
                fo.write("\t\t\"pk\": "+ str(d[1][0])+ ",\n")
                fo.write("\t\t\"fields\": {\n")
                fo.write("\t\t\t\"first_name\": \""+ d[1][1]+ "\",\n")
                fo.write("\t\t\t\"last_name\": \""+ d[1][2]+ "\"\n")
                fo.write("\t\t}\n")
                #end json item
                fo.write("\t}")
        # dump now movie table
        model_name="moviedb.movie"
        pk=0
        for m in movies:
                #begin json item
                if first:
                        first=False
                else:
                        fo.write(",\n")
                pk+=1
                fo.write("\t{\n")
                fo.write("\t\t\"model\": \""+ model_name+ "\",\n")
                fo.write("\t\t\"pk\": "+ str(pk)+ ",\n")
                fo.write("\t\t\"fields\": {\n")
                fo.write("\t\t\t\"director\": "+ str(m[0])+ ",\n")
                fo.write("\t\t\t\"title\": \""+ m[1]+ "\",\n")
                fo.write("\t\t\t\"comment\": \""+ m[2]+ "\"\n")
                fo.write("\t\t}\n")
                #end json item
                fo.write("\t}")

        #end json list
        fo.write('\n]\n')
        
        
        
        
        
                

