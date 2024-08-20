import sqlite3
import csv

# git -- global user.name "Sahil Koirala"
# git --global user.email "koirala24sahil@gmail.com"

# Create account in github
# git init
# git add .
# git commit -m"Your commit message"

# copy paste from gihub repository
# git remote add origin https://github.com/Runner-attacker/python_basic_project
# git push -u origin main

### after changing any file
# git status # check what happened in the file
# git diff
# git add .
# git commit -m "Your commit message"
# git push origin

def create_connection():
    try:
        con =  sqlite3.connect("users.sqlite3")
        return con
    except Exception as e:
        print(f"Error : {e}")


INPUT_STRING = """
    Enter the option:
    1. CREATE TABLE
    2. DUMP users from CSV INTO users TABLE
    3. ADD new user INTO users TABLE
    4. QUERY all users FROM the TABLE
    5. QUERY users by ID FROM the TABLE
    6. QUERY specified no. of records from TABLE
    7. DELETE all users
    8. DELETE user by id
    9. UPDATE user
    10. PRESS any key to EXIT
"""

def create_table(conn):
    CREATE_USERS_TABLE_QUERY = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name CHAR(255) NOT NULL,
            last_name CHAR(255) NOT NULL,
            company_name CHAR(255) NOT NULL,
            address CHAR(255) NOT NULL,
            city CHAR(255) NOT NULL,
            county CHAR(255) NOT NULL,
            state CHAR(255) NOT NULL,
            zip REAL NOT NULL,
            phone1 CHAR(255) NOT NULL,
            phone2 CHAR(255),
            email CHAR(255) NOT NULL,
            web text
        )
""" 
    cur = conn.cursor()
    cur.execute(CREATE_USERS_TABLE_QUERY)
    print("User Table was created sucessfully") 

def read_csv():
    users = []
    con = create_connection
    with open("sample_users.csv","r",newline="") as f:
        data = csv.reader(f)
        for user in data:
            users.append(tuple(user))
        return users[1:]
    
COLUMNS = (
            "first_name",
            "last_name",
            "company_name",
            "address",
            "city",
            "county",
            "state",
            "zip",
            "phone1",
            "phone2",
            "email",
            "web"
)
    
def insert_users(con,users):
    user_add_query = """
        INSERT INTO users 
        (
            first_name,
            last_name,
            company_name,
            address,
            city,
            county,
            state,
            zip,
            phone1,
            phone2,
            email,
            web
        )
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
    """
    cur = con.cursor()
    cur.executemany(user_add_query,users)
    con.commit()
    print(f"{len(users)} users were imported sucessfully")
 
def query_all_user(con):
    cur = con.cursor()
    users = cur.execute("SELECT * FROM users")
    for user in users:
        print(user)

def query_user_by_id(con,id):
    cur = con.cursor()
    user = cur.execute("SELECT * FROM users WHERE id=?",(id,))
    for i in user:
        print(i)
        
def query_specified_no_of_record(conn,number=0):
    cur = conn.cursor()
    if number:
        users = cur.execute("SELECT * FROM users LIMIT ?",(number,))
    else:
        users = cur.execute("SELECT * FROM users")
    for user in users:
        print(user)

def delete_users(con,id = 0):
    cur = con.cursor()
    if id:
        cur.execute("DELETE FROM users where id = ?",(id,))
        con.commit()
        print(f"User having id {id}  is deleted")
    else:
        cur.execute("DELETE FROM users")
        con.commit()
        print("All users are Deleted")
        
        
def update_user_by_id(con,user_id,column_name,column_value):
    update_query = f"UPDATE users set {column_name}=? where id=?;"
    cur = con.cursor()
    cur.execute(update_query,(column_value,user_id))
    con.commit()
    print(
        f"[{column_name}] was updated with value [{column_value}] of user with id [{user_id}]"
    )

def main():
    con = create_connection()
    user_input = int(input(INPUT_STRING))
    if user_input == 1:
        create_table(con)
    
    elif user_input == 2:
       users =  read_csv()
       insert_users(con=con,users=users)
    
    elif user_input ==3 :
        data = []
        for column in COLUMNS:
            column_value = input(f"Enter the value of {column} : ")
            data.append(column_value)
        insert_users(con,[tuple(data)])
    
    elif user_input == 4:
        query_all_user(con)       
    
    elif user_input == 5:
        id = input("ID : ")
        if id.isnumeric():
            query_user_by_id(con=con,id=id) 
    
    elif user_input == 6:
        no_of_user = input("Enter the number of user to fetch : ")
        if no_of_user.isnumeric() and int(no_of_user)>0 :
            query_specified_no_of_record(con,no_of_user)
    
    elif user_input == 7:
        confirm = input("Do you want to delete all users (y/n) : ")
        if confirm == 'y':
            delete_users(con)
    
    elif user_input == 8:
        id = input("Enter which id is to be deleted : ")
        if id.isnumeric() and int(id)>0:
            delete_users(con,id = int(id))
        
    elif user_input == 9:
        user_id = input("Enter id of user : ")
        if user_id.isnumeric():
            column_name = input(f"Enter the column you want to edit with in the given option {COLUMNS}")
            if column_name in COLUMNS:
                column_value = input(f"Enter the value of {column_name} : ")
                update_user_by_id(con,user_id,column_name,column_value)

main()

