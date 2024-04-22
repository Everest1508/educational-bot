import csv

def find_user_details(target_id):
    with open('user_data.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['id'] == target_id:
                return row
    return None

def save_to_db(user_data):
    fieldnames = ['id', 'username', 'first_name', 'last_name']
    with open('user_data.csv', 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(user_data)

def save_history(user_data):
    fieldnames = ['id', 'message', 'answered']
    with open('history.csv', 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(user_data)
