# importing libraries:
import json

# Function for Loading and Reading JSON File:
def load_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

# Loading and reading JSON Data:
data = load_data('data.json')

# function to display users and their connections:
def display_user(data):
    for user in data['user']:
        print(f'{user['id']}:{user['name']} is friends with: {user['friends']}')

    for page in data['pages']:
        print(f'{page['id']}:{page['name']}')

display_user(data)

# Function for cleaning JSON data:
def clean_data(data):
    # remove users with missing names:
    data['user'] = [user for user in data['user'] if user['name'].strip()]

    # remove duplicate friends:
    for user in data['user']:
       user['friends'] = list(set(user['friends'])) 

    # remove inactive users:
    data['user'] = [user for  user in data['user'] if user['friends'] or user['liked_pages']]

    # Remove duplicate pages:
    unique_pages = {}
    for page in data['pages']:
        unique_pages[page['id']] = page
    data['pages'] = list(unique_pages.values())
    return data

# load the data:
data = json.load(open('data2.json'))
data = clean_data(data)
json.dump(data, open('cleaned_data1.json','w'), indent=4)
print('Data has been cleaned successfully')


# Function for finding people you may know
def find_people_you_may_know(user_id, data):
    user_friends = {}
    for user in data['users']:
        user_friends[user['id']] = set(user['friends'])

    if user_id not in user_friends:
        return
    
    direct_friends = user_friends[user_id]
    suggestion = {}

    for friend in direct_friends:
        for mutual in user_friends[friend]:
            if mutual != user_id and mutual not in direct_friends:
                suggestion[mutual] = suggestion.get(mutual,0) + 1
    
    sorted_suggestions = sorted(suggestion.items(), key=lambda x:x[1],reverse=True)

    return [user_id for user_id, mutual_count in sorted_suggestions]

# Function for find page you may like
def find_pages_you_may_like(user_id,data):
    user_pages = {}

    for user in data['users']:
        user_pages[user['id']] = set(user['liked_pages'])

    if user_id not in user_pages:
        return
    
    user_liked_pages = user_pages[user_id]
    page_suggestion = {}

    for other_user, pages in user_pages.items():
        if other_user != user_id:
            shared_pages = user_liked_pages.intersection(pages)
        for page in pages:
            if page not in user_liked_pages:
                page_suggestion[page] = page_suggestion.get(page,0) + len(shared_pages)
    
    sorted_pages = sorted(page_suggestion.items(),key=lambda x: x[1],reverse=True)

    return [(page_id,score) for page_id,score in sorted_pages]