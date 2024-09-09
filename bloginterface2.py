
import bcrypt
import json
import os

# File paths
USER_FILE = 'users.json'
BLOG_FILE = 'blogs.json'

# function to read JSON data
def load_data():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as file:
            return json.load(file)
    return {}
# function to write into JSON file with proper spacing
def save_data(data):
    with open(USER_FILE, 'w') as file:
        json.dump(data, file, indent=4)
# function to load data from BLOG_FILE
def load_blogs():
    if os.path.exists(BLOG_FILE):
        with open(BLOG_FILE, 'r') as file:
            return json.load(file)
    return {}
# function to write into BLOG_FILE
def save_blogs(data):
    with open(BLOG_FILE, 'w') as file:
        json.dump(data, file, indent=4)
# Getting inputs from user and storing into data file
def register():
    users = load_data()
    username = input("Enter username: ")
    if username in users:
        print("Username already exists.")
        return

    password = input("Enter password: ")
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    users[username] = hashed_password.decode('utf-8')
    save_data(users)
    print("Registration successful!")

def login():
    users = load_data()
    username = input("Enter your username: ")
    if username not in users:
        print("Username does not exist.")
        return None

    password = input("Enter the  password: ")
    hashed_password = users[username].encode('utf-8')

    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        print("Login successful!")
        return username
    else:
        print("Invalid password.")
        return None
# creating and making alterations to the corresponding blog file of the user
def create_post(username):
    blogs = load_blogs()
    title = input("Enter the title of the post: ")
    if title in blogs.get(username, {}):
        print("Post with this title already exists.")
        return

    content = input("Enter post content: ")
    if username not in blogs:
        blogs[username] = {}
    blogs[username][title] = content
    save_blogs(blogs)
    print("Post created successfully!")

def delete_post(username):
    blogs = load_blogs()
    title = input("Enter the title of the post to be deleted: ")
    if username not in blogs or title not in blogs[username]:
        print("Post not found.")
        return

    del blogs[username][title]
    if not blogs[username]:
        del blogs[username]
    save_blogs(blogs)
    print("Post deleted successfully!")

def modify_post(username):
    blogs = load_blogs()
    title = input("Enter the title of the post to modify: ")
    if username not in blogs or title not in blogs[username]:
        print("Post not found.")
        return

    new_content = input("Enter new content: ")
    blogs[username][title] = new_content
    save_blogs(blogs)
    print("Post updated successfully!")
# the first interface displayed to the user
def main():
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            register()
        elif choice == '2':
            username = login()
            if username:
                while True:
                    print("\n1. Create Post")
                    print("2. Delete Post")
                    print("3. Modify Post")
                    print("4. Logout")
                    action = input("Choose an action: ")

                    if action == '1':
                        create_post(username)
                    elif action == '2':
                        delete_post(username)
                    elif action == '3':
                        modify_post(username)
                    elif action == '4':
                        print("Logged out successfully !")
                        break
                    else:
                        print("Invalid choice.")
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
