from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID
import csv


client = Client()
client.set_endpoint('https://cloud.appwrite.io/v1')
client.set_project('6557d0f6f0454be2134d')
client.set_key('d903e1bc1824eb8cfd7ce06c6d655e42425819166d6e399dadb6524875704dd8323f88b155a76cc9718b108ba0961beb12ad1ff7684ddcee873a00310a33a64adaf6f86375f0e66ecf7f17c9b157092bc5dee0b2a12cb7e3f0d16e68aff59f5f370f1eb97cd5d4443599cbd520dda2e185d9ac8dee35df3ef92e4bfcb99d3613')

databases = Databases(client)



with open('recipes_example.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)

    for row in reader:
        data = {}

        for i, header_field in enumerate(header):
            if header_field in ["Bestseller", "FamilyFriendly", "GlutenFree", "LactoseFree", "Vegan", "Vegatarian"]:
                if row[i] == 0:
                    row[i] = False
                else:
                    row[i] = True

            data[header_field] = row[i] 
        
            
        
        print(f"{row}:", data)
        result = databases.create_document('recipes', 'europe', ID.unique(), data)

csvfile.close()





# # Check if the document was created successfully
# if result.status == 200:
#     print('Document created successfully')
#     print(result.data)
# else:
#     print('Error creating document:', result.error.message)



# todoDatabase = None
# todoCollection = None

# def prepare_database():
#   global todoDatabase
#   global todoCollection

#   todoDatabase = databases.create(
#     database_id=ID.unique(),
#     name='TodosDB'
#   )

#   todoCollection = databases.create_collection(
#     database_id=todoDatabase['$id'],
#     collection_id=ID.unique(),
#     name='Todos'
#   )

#   databases.create_string_attribute(
#     database_id=todoDatabase['$id'],
#     collection_id=todoCollection['$id'],
#     key='title',
#     size=255,
#     required=True
#   )

#   databases.create_string_attribute(
#     database_id=todoDatabase['$id'],
#     collection_id=todoCollection['$id'],
#     key='description',
#     size=255,
#     required=False,
#     default='This is a test description.'
#   )

#   databases.create_boolean_attribute(
#     database_id=todoDatabase['$id'],
#     collection_id=todoCollection['$id'],
#     key='isComplete',
#     required=True
#   )


# #Add documents

# def seed_database():
#   """Create a function to add some mock data into your new collection"""
#   testTodo1 = {
#     'title': "Buy Lemons",
#     'description': "At least 2KGs",
#     'isComplete': True
#   }

#   testTodo2 = {
#     'title': "Wash the Lemons", 
#     'isComplete': True
#   }

#   testTodo3 = {
#     'title': "Cut the Lemons",
#     'description': "Don\'t forget to pack them in a box",
#     'isComplete': False
#   }

#   databases.create_document(
#     database_id=todoDatabase['$id'],
#     collection_id=todoCollection['$id'],
#     document_id=ID.unique(),
#     data=testTodo1
#   )

#   databases.create_document(
#     database_id=todoDatabase['$id'],
#     collection_id=todoCollection['$id'],
#     document_id=ID.unique(),
#     data=testTodo2
#   )

#   databases.create_document(
#     database_id=todoDatabase['$id'],
#     collection_id=todoCollection['$id'],
#     document_id=ID.unique(),
#     data=testTodo3
#   )



# #Retrieve documents

# def get_todos():
#   """Create a function to retrieve the mock todo data, then execute the functions in _main_."""
#   todos = databases.list_documents(
#     database_id=todoDatabase['$id'],
#     collection_id=todoCollection['$id']
#   )
#   for todo in todos['documents']:
#     print(f"Title: {todo['title']}\nDescription: {todo['description']}\nIs Todo Complete: {todo['isComplete']}\n\n")

# if __name__ == "__main__":
#   prepare_database()
#   seed_database()
#   get_todos()
