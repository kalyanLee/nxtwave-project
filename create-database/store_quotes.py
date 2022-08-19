import json
import sqlite3

# Connecting to sqlite
connection = sqlite3.connect('quotes.db')


#creat a cursor object
cursor_obj = connection.cursor()

def create_author_table():
    # Delete the author table if already exists.
    cursor_obj.execute("DROP TABLE IF EXISTS author")

    # Creating a authors table 
    author_table = '''CREATE TABLE author (
                author_id INTEGER PRIMARY KEY NOT NULL,
                name VARCHAR(255) NOT NULL,
                born_details TEXT,
                reference TEXT
            );'''
    
    cursor_obj.execute(author_table)                                        


def insert_values_of_author_table(authors_details):                                       
    # insert Data into author table
    for i in range(len(authors_details)):
        insert_values = (i+1, authors_details[i]['name'], authors_details[i]['born'],authors_details[i]['reference'])
        cursor_obj.execute("INSERT INTO author VALUES (?,?,?,?)", insert_values)

def create_quote_table():
    # Delete the quote table if already exists.
    cursor_obj.execute("DROP TABLE IF EXISTS quote")

    # Creating a quote table 
    quote_table = '''CREATE TABLE quote (
                quote_id INTEGER PRIMARY KEY NOT NULL,
                quote TEXT NOT NULL,
                author_id INTEGER
            );'''
    
    cursor_obj.execute(quote_table)   


def get_author_id(name):
    cursor_obj.execute('SELECT author_id FROM author WHERE name=?', (name,))
    author_id = cursor_obj.fetchone()[0]
    return author_id
    
def insert_values_of_quote_table(quotes_details):                                       
    # insert Data into quote table
    for i in range(len(quotes_details)):
        author_id = get_author_id(quotes_details[i]['author'])
        insert_values = (i+1, quotes_details[i]['quote'], author_id)

        cursor_obj.execute("INSERT INTO quote VALUES (?,?,?)", insert_values)
         

def create_tag_table():
    # Delete the tag table if already exists.
    cursor_obj.execute("DROP TABLE IF EXISTS tag")

    # Creating a tag table 
    tag_table = '''CREATE TABLE tag (
                tag_id INTEGER PRIMARY KEY NOT NULL,
                tag VARCHAR(255) NOT NULL,
                quote_id INTEGER
            );'''
    
    cursor_obj.execute(tag_table) 


def insert_values_of_tag_table(quotes_details): 

    # insert Data into tags table
    k=1
    for i in range(len(quotes_details)):
        tag_list = quotes_details[i]['tags']
        for j in range(len(tag_list)):
            insert_values = (k, tag_list[j], i+1)
            cursor_obj.execute("INSERT INTO tag VALUES (?,?,?);", insert_values)
            k += 1



# open json file and convert dict object
file = open("../webscrapping/quotes.json", "r")
json_file = file.read() 

quotes_and_author_dict = json.loads(json_file)

quotes_details = quotes_and_author_dict['quotes']
authors_details = quotes_and_author_dict['authors']

# call the above functions
create_author_table()
connection.commit() #commit the changes in db

insert_values_of_author_table(authors_details)
connection.commit()

create_quote_table()
connection.commit()

insert_values_of_quote_table(quotes_details)
connection.commit()

create_tag_table()
connection.commit()

insert_values_of_tag_table(quotes_details)
connection.commit()

# Close the connection
connection.close()
