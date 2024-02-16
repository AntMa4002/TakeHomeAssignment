import requests
import sqlite3

# Performing API call using the request library
response = requests.get('https://dog.ceo/api/breeds/list/all')
data = response.json()

print("Retrieving Data from Dog API Complete")

breedsInfo = data['message']

conn = sqlite3.connect('dog_breeds.db')
c = conn.cursor()

print("Inserting Data into a SQLITE Database and connecting to it Complete")

c.execute('''CREATE TABLE IF NOT EXISTS breedsInfo (breed_name TEXT, sub_breed_name TEXT)''')

print("Creating table for breedsInfo and sub-breeds Complete")

for breed, sub_breeds in breedsInfo.items():
    for sub_breed in sub_breeds:
        c.execute('INSERT INTO breedsInfo (breed_name, sub_breed_name) VALUES (?, ?)', (breed, sub_breed))

print("Inserting data into table Complete")

conn.commit()
print("Commit Transaction Complete")

# Create the 'sub_breed_count' table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS sub_breed_count (breed_name TEXT UNIQUE, sub_breed_count INTEGER)''')
print("New table called sub_breed_count creation Complete")

# Insert data into 'sub_breed_count' table, ignoring duplicates
c.execute('''
    INSERT OR IGNORE INTO sub_breed_count (breed_name, sub_breed_count)
    SELECT breed_name, COUNT(sub_breed_name) FROM breedsInfo GROUP BY breed_name
''')
print("Data insertion into the table Complete")

# Commit the transaction and close the connection
conn.commit()

print("File insertion Complete")

select_query = 'SELECT * FROM sub_breed_count'

print("Executing the query Complete")
c.execute(select_query)

rows = c.fetchall()
print("Fetching rows Complete")

# Display the results
for row in rows:
    print(row)

# Close the connection
conn.close()