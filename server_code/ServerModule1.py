import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#


#Store post data using a server function
@anvil.server.callable
def add_post(post_title, text, image):
  import uuid
  app_tables.cards.add_row(
    Card_name=post_title, 
    Content=text, 
    Created=datetime.now(),
    image=image,
    post_id = str(uuid.uuid4())
    
    
  )
@anvil.server.callable
def get_post():
  # Get a list of post from the Data Table, sorted by 'created' column, in descending order
  return app_tables.cards.search(
    tables.order_by("Created", ascending=False)
  )

@anvil.server.callable
def update_post(row, post_title, text, image):
  #updata a card
  row['Card_name'] = post_title
  row['Content'] = text
  row['image'] = image


