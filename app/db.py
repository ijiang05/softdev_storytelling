# POPEYES: Lauren Lee, Vivian Teo, Ian Jiang
# SoftDev
# P00 -- Storytelling
# 2022-11-15
# time spent: 23.3

import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O


# # delete table if needed (testing purposes)
# DB_FILE="edits.db"
# db = sqlite3.connect(DB_FILE) 
# c = db.cursor() 
# # c.execute("DELETE FROM edits")
# # # c.execute("DELETE FROM users")

# table = c.execute("SELECT * from edits")
# print(table.fetchall())

# db.commit()
# db.close()

'''
Used for both users.db and edits.db
creates users.db and edits.db if it does not already exists
'''
def create_tables():
    # users table
    DB_FILE="users.db"

    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
    # users table
    c.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT, pw TEXT, id_list TEXT, editing TEXT)")
    
    db.commit() #save changes
    db.close()  #close database

    # edits table
    DB_FILE="edits.db"

    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

    c.execute("CREATE TABLE IF NOT EXISTS edits(id INTEGER PRIMARY KEY, title TEXT, content TEXT, time TEXT, latest_change TEXT)")
    
    db.commit() #save changes
    db.close()  #close database

'''
Used for user.db
Adds users who have registered into the database
'''
def add_user(user, passw):
    DB_FILE="users.db"

    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

    # add newly registered people in
    c.execute("INSERT INTO users (name, pw) VALUES (?,?)", (user, passw))
    
    #prints users table
    table = c.execute("SELECT * from users")
    print("user table from add_user() call")
    print(table.fetchall())

    db.commit() #save changes
    db.close()  #close database

'''
Used for user.db
checks if user is already in the database prior to registration
'''
def user_does_not_exists(user):
    DB_FILE="users.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
    
    namie = c.execute("SELECT name FROM users WHERE name = ?", (user,)).fetchone()
    # print(namie)
    if namie is None:
        exists = False
    else:
        exists = True

    # prints users table
    table = c.execute("SELECT * from users")
    print("user table from user_does_not_exists() call")
    print(table.fetchall())
    
    print(exists)

    db.commit() #save changes
    db.close()  #close database
    return exists == False

'''
Used for user.db
Checks if login credentials match any in the database
'''
def valid_login(user, passw):
    DB_FILE="users.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
    
    # check if username is in table
    namie = c.execute("SELECT name FROM users WHERE name = ?", (user,)).fetchone()
    print("print if user that matches inputed user, none if no match")
    print(namie)
    if namie is None:
        exists = False
    else:
        exists = True

    # check if password is in table
    passie = c.execute("SELECT pw FROM users WHERE pw =?", (passw,)).fetchone()
    print("print if pw that matches inputed pw, none if no match")
    print(passie)
    if passie is None:
        exists = False

    # prints table
    table = c.execute("SELECT * from users")
    print("user table from valid_login() call")
    print(table.fetchall())
    
    print("whether or not login exists")
    print(exists)

    db.commit() #save changes
    db.close()  #close database
    return exists
'''
Used for edits.db
Creates new story
'''
def create_story(title, text):
    DB_FILE="edits.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    #adds story into database
    data = [title, text, text]
    c.execute("INSERT INTO edits (title, content, latest_change) VALUES(?,?,?)", data)
   # c.execute(f"INSERT INTO edits (title, content, time, latest_change) VALUES ('{title}', '{text}', '{ctime()}', '{text}')")
   
    #print content into terminal
    print("contents of story when created")
    print(c.execute("SELECT content FROM edits").fetchall())
    
    db.commit() #save changes
    db.close() #close database

'''
Used for edits.db and user.db
Adds the story the user contributed to to their id_list
'''
def add_to_contributed(title, user):
    DB_FILE="users.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    current_id = get_id(title) #get the id of the story the user contributed to
    print("printing id of the title user contributed to")
    print(current_id)
    
    id_list = str(c.execute("SELECT id_list FROM users WHERE name = ?", (user,)).fetchone()[0]) #get current list of ids the user has contributed to
    print("printing id list")
    print(id_list)

    if id_list == "None": #check if list is empty
        print("id list is empty")
        c.execute("UPDATE users SET id_list = ? WHERE name = ?", (current_id, user))
    else:
        current_id = id_list + "," + current_id #add newly contributed story to the list
        c.execute("UPDATE users SET id_list = ? WHERE name = ?", (current_id, user))
    
    print("all id lists")
    print(c.execute("SELECT id_list FROM users").fetchall())

    db.commit()
    db.close()
    
'''
Used for edits.db
Gets id of inputed story
    used for add_to_contributed(id,user)
'''
def get_id(title):
    DB_FILE="edits.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    #get id of story with given title
    current_id = c.execute("SELECT id FROM edits WHERE title = ?", (title,)).fetchone()

    db.commit()
    db.close()
    return str(current_id[0])

'''
Used for edits.db
Checks if story exists
'''
def story_does_not_exist(title):
    DB_FILE="edits.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
    
    titlie = c.execute("SELECT title FROM edits WHERE title = ?", (title,)).fetchone()
    if titlie is None:
        exists = False
    else:
        exists = True
    
    db.commit() #save changes
    db.close()  #close database
    return exists == False

'''
Used for edits.db
outputs a dict containing all the stories user contributed to
'''
def all_stories_contributed_to(user):
    DB_FILE="users.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    id_list = str(c.execute('SELECT id_list FROM users WHERE name = ?', (user,)).fetchone()[0])
    print("id list of user")
    print(id_list)

    if id_list == 'None':
        id_list = []
    else:
        id_list = id_list.split(",")

    print("id list of user as list")
    print(id_list) #list of ids of all titles user contributed to

    db.commit() #save changes
    db.close()  #close database

    #now that we have a dict of the story ids the user has contributed to, we can close users.db and extract the content from edits.db
    DB_FILE="edits.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    #our final output (huge string)
    final_dict = {}

    if id_list == []:
        db.commit() #save changes
        db.close()  #close database
        return final_dict
    else:
    # for each story id in the list, we'll extract the title + content out and put it in final_text
        for story_id in id_list:
            print("story id in id list:" + story_id)
            #title
            title = c.execute("SELECT title FROM edits WHERE id = ?", (story_id,)).fetchone()[0]
            #content
            content = c.execute("SELECT content FROM edits WHERE id = ?", (story_id,)).fetchone()[0]
            #story id
            id = c.execute("SELECT id FROM edits WHERE id = ?", (story_id,)).fetchone()[0]
        #add to dict
            final_dict[id] = [title, content]
        db.commit() #save changes
        db.close()  #close database
        return final_dict
# print(all_stories_contributed_to("ian"))
# all_stories_contributed_to("ian")

"""
used to see if the user has contributed to story with id of story_id
"""
def has_contributed_to(user, story_id):
    all_contributed = all_stories_contributed_to(user)
    print("calling has_contributed_to()")
    print(all_contributed)
    for x in all_contributed: #for each id in all_contributed, see if story_id equals the id.
        print(type(x))
        print("what is key of all_contributed")
        print(x)
        if int(x) == int(story_id):
            return True
    return False

"""
used in edits.db
returns the correct contents of the story the user should see
"""
def story_content(user, story_id):
    DB_FILE="edits.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    #depends on if user has contributed to a story or not
    if has_contributed_to(user, story_id): # if the user has contributed to story with id as story_id
        ret_val =  c.execute("SELECT content FROM edits WHERE id = ?", (story_id,)).fetchone()[0] # return full story
    else:
        ret_val = c.execute("SELECT latest_change FROM edits WHERE id = ?", (story_id,)).fetchone()[0] # else return latest change to story
    db.commit() #save changes
    db.close()  #close database
    return ret_val

"""
used in edits.db
returns title of story with id of story_id
"""
def get_title(story_id):
    DB_FILE="edits.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    title = c.execute("SELECT title FROM edits WHERE id = ?", (story_id,)).fetchone()[0]
    db.commit() #save changes
    db.close()  #close database

    return title

"""
used in edits.db
returns a dict for all the stories in the database to be displayed in the table of contents
"""
def get_all_stories(user):
    DB_FILE="edits.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    #fetches all stories from edits
    all_stories = c.execute("SELECT title FROM edits").fetchall()
    for tupl in range(len(all_stories)):
        ret_tupl = ""
        for y in all_stories[tupl]:
            ret_tupl = ret_tupl + y
        all_stories[tupl] = ret_tupl

    #assumes title is same but we should allow diff
    user_view = {}
    for x in all_stories:
        print("each title")
        print(x)
        id = c.execute("SELECT id FROM edits WHERE title = ?", (x,)).fetchone()[0]
        user_view[x] = id
    db.commit() #save changes
    db.close()  #close database

    return user_view

"""
used in edits.db
adds text to an already existing story with the inputed id. updates content and latest_change for the story and id_list for the user
"""
def edit_story(user,text,id):
    DB_FILE="edits.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()    

    print("id of story")
    print(id)
    # add to edits the latest change and replace content
    content = c.execute("SELECT content FROM edits WHERE id = ?", (id,)).fetchone()[0]
    content += " " + text
    c.execute("UPDATE edits SET latest_change = ? WHERE id = ?", (text, id))
    c.execute("UPDATE edits SET content = ? WHERE id = ?", (content, id))

    # add this story to the list of contributed in users.db
    title = c.execute("SELECT title FROM edits WHERE id = ?", (id,)).fetchone()[0]
    add_to_contributed(title, user) # update the list of contributed stories

    db.commit() #save changes
    db.close()  #close database

'''
# with open('students.csv', newline='') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         c.execute("INSERT INTO students VALUES ('" + row['name'] + "', " + row['age'] + "," + row['id'] + ")")
students_table = c.execute("SELECT * FROM students")
print(students_table.fetchall())
# courses table
DB_FILE="courses.db"
db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
db.execute("DROP TABLE if exists courses")
c.execute("CREATE TABLE courses(code TEXT, mark INTEGER, id INTEGER)")
with open('courses.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        c.execute("INSERT INTO courses VALUES ('" + row['code'] + "', " + row['mark'] + "," + row['id'] + ")")
courses_table = c.execute("SELECT * FROM courses")
'''


# command = ""          # test SQL stmt in sqlite3 shell, save as string
# c.execute(command)    # run SQL statement

#==========================================================