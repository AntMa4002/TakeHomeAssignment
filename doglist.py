import requests
import sqlite3

# Performing API call using the request library, specifically sends an HTTP GET request and retrieves the JSON response from the API
response = requests.get('https://dog.ceo/api/breeds/list/all')
data = response.json()
print("Retrieving Data from Dog API Successful")
print("..........................................")

# Extracts the message field which contains a dictionary of the breeds and their sub-breeds
breedsInfo = data['message']

# Connects to the database dog_breeds.db
dataBase = sqlite3.connect('dog_breeds.db')

# Initialized the cursor object to perform SQL commands (essentially mock commands normally performed in the SQL terminal but done through Python)
cursor = dataBase.cursor()

print("Database connection Successful")
print("..........................................")

# Check if the breeds info table already exists so that the table is not updated when performing multiple runs for testing
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='breedsInfo'")
breedsInfo_table_exists = cursor.fetchone()

# If the breedsInfo table does not exist, then the table is created and data is inserted
if not breedsInfo_table_exists:

    # Initialization of the breedsInfo table
    cursor.execute('''CREATE TABLE breedsInfo (breed_name TEXT, sub_breed_name TEXT)''')

    print("Creating table for breedsInfo Successful")
    print("..........................................")

    # Insertion of Data into the breedsInfo table from the response of the API call
    for breed, sub_breeds in breedsInfo.items():
        for sub_breed in sub_breeds:
            cursor.execute('INSERT INTO breedsInfo (breed_name, sub_breed_name) VALUES (?, ?)', (breed, sub_breed))

    print("Inserting data into table Successful")
    print("..........................................")

    # Commiting Changes to the Database
    dataBase.commit()
    print("Commit Successful")
    print("..........................................")

# Check if the sub_breed_count table already exists so that the table is not updated when performing multiple runs for testing
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sub_breed_count'")
sbCount_table_exists = cursor.fetchone()

# If the sub_breed_count table does not exist, then the table is created and data is inserted
if not sbCount_table_exists:
    # Initialization of the sub_breed_count table
    cursor.execute('''CREATE TABLE sub_breed_count (breed_name TEXT, sub_breed_count INTEGER)''')
    print("Creating new sub_breed_count table Successful")
    print("..........................................")

    # Inserting data into the sub_breed_count table from the breedsInfo data, specifically counting the length of the sub-breed arrays in the breedsInfo table
    cursor.execute('''
        INSERT INTO sub_breed_count (breed_name, sub_breed_count)
        SELECT breed_name, COUNT(sub_breed_name) FROM breedsInfo GROUP BY breed_name
    ''')
    print("Inserting data into table Successful")
    print("..........................................")

    # Commiting Changes to the Database
    dataBase.commit()
    print("Commit Successful")
    print("..........................................")

# Executes the SQL query to select all columns in the sub_breed_count table 
cursor.execute('SELECT * FROM sub_breed_count')

# Fetches the result of the query that was previously executed
rows = cursor.fetchall()
print("Fetching rows Successful")
print("..........................................\n")

print("Breed | Sub-Breed Count")
print("------------------------------------------")

# Displays the breeds and their sub-breed counts
for row,count in rows:
    print(row + ": " + str(count))

# Closes the connection to the Database
dataBase.close()