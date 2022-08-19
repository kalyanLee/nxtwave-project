import sqlite3

# Connecting to sqlite
connection = sqlite3.connect('../create-database/quotes.db')
  
# cursor object
cursor_obj = connection.cursor()

# create function that return the total no.of quotes in website 
def get_total_no_of_quotes():
    statement = '''SELECT count(quote_id) as total_quotes FROM quote;'''
    cursor_obj.execute(statement)
    total_quotes = cursor_obj.fetchone()[0]
    return total_quotes


# create a function that return No. of quotations authored by the given author’s name
def get_no_of_quotes_authored_by_author(author_name):
    statement = '''SELECT 
                    count(quote.quote_id) as number_of_quotes 
                FROM 
                    quote INNER JOIN author ON quote.author_id = author.author_id 
                where author.name = ?'''
    cursor_obj.execute(statement, (author_name,))
    number_of_quotes_by_given_author = cursor_obj.fetchone()[0]
    return number_of_quotes_by_given_author


# create a function that return Minimum, Maximum, and Average no. of tags on the quotations
def get_min_max_avg_no_of_tags():
    statement = '''SELECT 
                        MIN(no_of_tags) AS manimum_tags, 
                        MAX(no_of_tags) as maximum_tags, 
                        AVG(no_of_tags) as avg_tags 
                    FROM 
                        (SELECT COUNT(tag_id) As no_of_tags FROM tag 
                        GROUP BY quote_id);'''
    cursor_obj.execute(statement)
    query_result = cursor_obj.fetchone()

    return query_result


# create a function that return top N authors who authored the maximum number of quotations
def get_authors_who_authored_maxmimum_no_of_quotations(n):
    statement = '''SELECT 
                        author.name, COUNT(quote.quote_id) as no_of_quotes 
                    FROM 
                        'quote' INNER JOIN author ON quote.author_id = author.author_id  
                    GROUP BY 
                        quote.author_id 
                    ORDER BY 
                        no_of_quotes DESC 
                    LIMIT ?;'''
    cursor_obj.execute(statement, (n,))
    top_n_authors_list_of_tuples = cursor_obj.fetchall()

    # top_n_authors = []
    # for author_tuple in top_n_authors_list_of_tuples:
    #     top_n_authors.append(author_tuple)

    # return tuple(top_n_authors)
    return top_n_authors_list_of_tuples

# call the above functions
print(get_total_no_of_quotes())

print(get_no_of_quotes_authored_by_author("Albert Einstein"))

print(get_min_max_avg_no_of_tags())

print(get_authors_who_authored_maxmimum_no_of_quotations(5))

# Close the connection
connection.close() 
