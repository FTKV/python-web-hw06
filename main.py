import sqlite3
import os

from create_db import DATABASE


def execute_query(sql: str) -> list:
    with sqlite3.connect(DATABASE) as con:
        cursor = con.cursor()
        cursor.execute(sql)
        return cursor
    
        
def print_sql(cursor):
    results = cursor.fetchall()

    widths = []
    columns = []
    tavnit = '|'
    separator = '+'

    try:
        terminal_width = int(str(os.get_terminal_size()).split(",")[0].split("columns=")[1])
    except ValueError:
        terminal_width = 150
    end_of_width = 1
    for index, cd in enumerate(cursor.description):
        end_of_width += 3
        if end_of_width >= terminal_width:
            break
        max_col_length = max(list(map(lambda x: len(str(x[index])), results)))
        max_col_length = max(max_col_length, len(cd[0]))
        if end_of_width + max_col_length > terminal_width:
            max_col_length = terminal_width - end_of_width
        end_of_width += max_col_length
        widths.append(max_col_length)
        columns.append(cd[0])

    for w in widths:
        #tavnit += " %-"+"%ss |" % (w,)
        tavnit += " %-"+"%s.%ss |" % (w,w)
        separator += '-'*w + '--+'

    print(separator)
    print(tavnit % tuple(columns))
    print(separator)
    for row in results:
        print(tavnit % row)
    print(separator)


def read_query(number):
    with open('query_number.sql', 'r') as f:
        sql_list = f.read()
        return sql_list.split(";")[number-1]
    
    
if __name__ == "__main__":
    while True:
        user_input = input("Enter the number of query from 1 to 12 or 'exit': ")
        if user_input.strip().casefold() == "exit":
            exit(0)
        try:
            user_input = int(user_input)
        except ValueError as error:
            print("Try again")
            continue
        if not 1 <= user_input <= 12:
            print("Try again")
            continue
        sql = read_query(user_input)
        cursor = execute_query(sql)
        print_sql(cursor)
