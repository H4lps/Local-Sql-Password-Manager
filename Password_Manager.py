from tkinter import *; import hashlib; import sqlite3; from sqlite3 import Error
import time

#How we check if user signed in correctly
def sign_in_func(connection):
    b = hashlib.sha256(username.get("1.0", "end-1c").strip().encode()).hexdigest()
    d = hashlib.sha256(Password.get("1.0","end-1c").strip().encode()).hexdigest()
    cursor = connection.cursor()
    user_query = "SELECT user FROM users WHERE user = ?"
    pass_query = "SELECT pass FROM users WHERE user = ?"
    name_query = "SELECT name FROM users WHERE user = ?"
    id_query = "SELECT user_id FROM users WHERE user = ?"
    user_result = execute_query(connection, user_query, (b,))
    if user_result:
        pass_result = execute_query(connection,pass_query,(user_result[0][0],))
    name_query = execute_query(connection, name_query, (b,))
    id_query = execute_query(connection,id_query,(b,))
    if user_result and pass_result:
        if user_result[0][0] == b and pass_result[0][0] == d:
            sign_in.pack_forget()
            welcome(name_query[0][0],id_query[0][0])

def welcome(name,id):
    welcome_screen = Frame(tk)
    welcome_screen.pack()
    Label(welcome_screen,text=f"Welcome {name}!").pack()
    Label(welcome_screen, text="Web Info").pack()
    create_new = Button(welcome_screen,text="NEW",command=lambda : new_website(welcome_screen,id,name))
    create_new.pack(side="bottom")
    sites_query = "SELECT * FROM sites where user_id = ?"
    main_query = execute_query(connection, sites_query, (id,))
    for i in range(len(main_query)):
        Label(welcome_screen,text=f"site: {main_query[i][1]}").pack()
        Label(welcome_screen,text=f"User: {main_query[i][2]}").pack()
        Label(welcome_screen, text=f"Password: {main_query[i][3]}").pack()
    

    
def new_website(welcome_screen,id,name):
    welcome_screen.pack_forget()
    new_site = Frame(tk)
    new_site.pack()
    Label(new_site, text="ADD SITE").pack()
    Label(new_site, text="Site Name:").pack()
    site_name = Text(new_site,width=10,height=2)
    site_name.pack()
    Label(new_site, text="Username:").pack()
    site_user = Text(new_site,width=10,height=2)
    site_user.pack()
    Label(new_site,text="Password:").pack()
    site_pass =  Text(new_site,width=10,height=2)
    site_pass.pack()
    add_new_button = Button(new_site,width=10,height=5,text="add",command=lambda : add_new_stuff(site_name.get("1.0","end-1c").strip(),site_user.get("1.0","end-1c").strip(),site_pass.get("1.0","end-1c").strip(),id,new_site,name))
    add_new_button.pack()
def add_new_stuff(site, user, pas, id,n_frame,name):
    site_query = "INSERT into sites(user_id,site,site_user,site_pass) VALUES(?,?,?,?)"
    if site != "" or user != "" or pas != "":
        execute_query(connection,site_query,(id,site,user,pas))
        n_frame.pack_forget()
        welcome(name,id)
    else:
        error_message = Label(n_frame,text="Must fill out all fields")
        error_message.pack()
        n_frame.after(3000,error_message.pack_forget)
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection successful")
    except Error as e:
        print(f"The error is: {e}")
    return connection
def execute_query(connection, query, params = None):
    cursor = connection.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        connection.commit()
        print("Query executed successfully")
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
def new_user(connection):
    new_user_screen = Frame(tk)
    sign_in.pack_forget()
    new_user_screen.pack()
    Label(new_user_screen,font=("Arial", 30) ,text="NEW USER").pack()
    Label( new_user_screen,text="Username").pack()
    user_ans = Text(new_user_screen,width=10,height=2)
    user_ans.pack();
    Label(new_user_screen,text = "Password").pack()
    pass_ans = Text(new_user_screen,width=10,height=2)
    pass_ans.pack()
    Label(new_user_screen,text="Name").pack()
    name_ans = Text(new_user_screen,width=10,height=2)
    name_ans.pack()
    Label(new_user_screen,text="Age").pack()
    age_ans = Text(new_user_screen,width=10,height=2)
    age_ans.pack()
    Create_account = Button(new_user_screen, height=3, width=10, text="Create Account",fg= "gray", command=lambda : confirm_account(connection,new_user_screen,user_ans,pass_ans,name_ans,age_ans)).pack()

def confirm_account(connection,n_frame, user, password, name,age):
    user_check = check_user(connection,user)
    age = age.get("1.0", "end-1c").strip(); user  = user.get("1.0", "end-1c").strip(); password = password.get("1.0", "end-1c").strip(); name = name.get("1.0", "end-1c").strip();
    if user == "" or password == "" or name == "" or age == "":
        error_message = Label(n_frame,text="Must fill out all fields")
        error_message.pack(side=TOP)
        n_frame.after(3000,error_message.pack_forget)
    elif user_check == False:
        error_message = Label(n_frame, text="Username not available")
        error_message.pack(side=TOP)
        n_frame.after(3000, error_message.pack_forget)
    elif password_strength(password) != 2:
        error_message = Label(n_frame, text="Password is too weak")
        error_message.pack(side=TOP)
        n_frame.after(3000, error_message.pack_forget)
    elif not age.isdigit():
        error_message = Label(n_frame, text="Age must be an integer")
        error_message.pack(side=TOP)
        n_frame.after(3000, error_message.pack_forget)
    else:
        create_query = "INSERT INTO users(user,pass,name,age) VALUES(?,?,?,?)"
        encode_u = hashlib.sha256(user.encode()).hexdigest()
        encode_p = hashlib.sha256(password.encode()).hexdigest()
        execute_query(connection,create_query, (encode_u,encode_p,name,int(age)))
        n_frame.pack_forget()
        startup(tk,connection)
        
    
def check_user(connection,user):
    b = hashlib.sha256(user.get("1.0", "end-1c").strip().encode()).hexdigest()
    user_query = "SELECT user FROM users WHERE user = ?"
    found_user = execute_query(connection, user_query, (b,))
    if not found_user:
        return True
    return False
def password_strength(password):
    counter = 0
    if any(letter.isdigit() for letter in password):
        counter += 1
    if len(password) >= 5:
        counter += 1
    return counter
create_users_table = """
CREATE TABLE users(
user_id INTEGER PRIMARY KEY,
user TEXT NOT NULL,
pass TEXT NOT NULL,
name TEXT NOT NULL,
age INTEGER
);
"""
create_users = '''
INSERT INTO
    users(user_id,user, pass, name, age)
Values
    (NULL,'dbfa2eaaa22a6cf5b73c2b9f5b6682f337a9d1bd2f8847709accb2ceed3b7045', 'fc865f46ca2655bb5f4986ec69d9b9029185cd83afb1adcb087f65d5b86df7d9', 'Liam', '40'),
    (NULL,'4b8d14b2b50409d06b0ca885152481dcac309157e7c25eb44c5566d4fd0a08af','29c586fe7c24a1380f5f343050e6094f4850f42363b585505b366e60e82d4ab6', 'BigLiam','20')
'''
create_sites_table ='''
CREATE TABLE sites(
user_id INTEGER NOT NULL,
site TEXT NOT NULL,
site_user TEXT NOT NULL,
site_pass TEXT NOT NULL,
FOREIGN KEY (user_id) REFERENCES users(user_id)
)
'''

def delete_data(connection):
    cur = connection.cursor()
    connection.commit()
    cur.execute("DROP TABLE IF EXISTS users")
    connection.commit()
def print_users(connection):
    cur = connection.cursor()
    cur.execute("SELECT * FROM users")
    print(cur.fetchall())
def startup(root,connection):
    sign_in=Frame(root)
    sign_in.pack()
    Label(sign_in, text="Sign In",font=("Arial",30)).pack()
    Label(sign_in, text="Username", width=10, height=2).pack()
    username = Text(sign_in, height=2,width=30)
    username.pack()
    Label(sign_in, text="Password", height=2).pack()
    Password = Text(sign_in, height=2,width=30,)
    Password.pack()
    sign_in_button = Button(sign_in, height=5, width=10, text="SIGN IN",fg= "gray", command=lambda : sign_in_func(connection)).pack()
    new_user_button = Button(sign_in,height=2, width=5,text="New User", fg="gray",command=lambda : new_user(connection)).pack()

#Sign In window
if __name__ == "__main__":
    connection = create_connection("E:\\sm_app.sqlite")
    #delete_data(connection)
    #execute_query(connection,create_users_table)
    #execute_query(connection,create_sites_table)
    #execute_query(connection,create_users)
    #print(execute_query(connection,"SELECT * from sites"))
    #print_users(connection)
    #print(execute_query(connection, "SELECT user_id FROM users"))
    tk =  Tk()
    tk.title("Password Manager")
    tk.geometry("350x350")

    sign_in=Frame(tk)
    sign_in.pack()
    Label(sign_in, text="Sign In",font=("Arial",30)).pack()
    Label(sign_in, text="Username", width=10, height=2).pack()
    username = Text(sign_in, height=2,width=30)
    username.pack()
    Label(sign_in, text="Password", height=2).pack()
    Password = Text(sign_in, height=2,width=30,)
    Password.pack()
    sign_in_button = Button(sign_in, height=5, width=10, text="SIGN IN",fg= "gray", command=lambda : sign_in_func(connection)).pack()
    new_user_button = Button(sign_in,height=2, width=5,text="New User", fg="gray",command=lambda : new_user(connection)).pack()





    tk.mainloop()






