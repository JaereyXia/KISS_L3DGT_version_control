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


@anvil.server.callable
def search_posts(keyword):
  import difflib

  # Split the user's search into separate words
  # Example: "school holiday"
  # becomes ["school", "holiday"]
  keywords = keyword.lower().split()

  # Store matching posts
  results = []

  # Loop through every post in Data Table
  for row in app_tables.cards.search():

    # Get title and content
    # If blank, use "" to avoid errors
    title = (row['Card_name'] or "").lower()
    content = (row['Content'] or "").lower()

    # Score system:
    # higher score = better search match
    score = 0

    # Check every keyword user typed
    for word in keywords:

      # -------------------------
      # Normal contains search
      # -------------------------

      # If keyword exists in title,
      # add higher score
      if word in title:
        score += 5

        # If keyword exists in content,
        # add smaller score
      if word in content:
        score += 3

        # -------------------------
        # Fuzzy search (typo fixing)
        # Example:
        # "schol" -> "school"
        # -------------------------

        # Split title into words
      title_words = title.split()

      # Split content into words
      content_words = content.split()

      # Check title words similarity
      for title_word in title_words:

        similarity = difflib.SequenceMatcher(None, word, title_word).ratio()

        # If similarity is high enough,
        # count as a match
        if similarity > 0.75:
          score += 3

          # Check content words similarity
      for content_word in content_words:

        similarity = difflib.SequenceMatcher(None, word, content_word).ratio()

        # If similarity is high enough,
        # add smaller score
        if similarity > 0.75:
          score += 1

        # If score is more than 0,
        # save the post
    if score > 0:
      results.append((score, row))

    # Sort results by highest score first
    # Most relevant post appears on top
  results.sort(
    reverse=True,
    key=lambda x: x[0]
  )

  # Return only rows
  return [row for score, row in results]


  #set all the user that just sign up a start role of student
  @anvil.server.callable
  def create_profile(user):
    app_tables.profiles.add_row(
      user=user,
      role="student"
    )


  #Get user's role
  @anvil.server.callable
  def get_user_role():
    user = anvil.users.get_user()
    profile = app_tables.profiles.get(user = user)
    return profile['role']

  
  @anvil.server.callable
  def update_post(
    row,
    post_title,
    text,
    image
  ):
  
    user = anvil.users.get_user()
  
    profile = app_tables.profiles.get(
      user=user
    )
  
    role = profile['role']
  
    # Check permission
    is_owner = (
      row['creator'] == user
    )
  
    is_teacher = (
      role == "teacher"
    )
  
    if not (is_owner
      or is_teacher
    ):
  
      raise Exception("No permission.")
  
      # Update post
    row['Card_name'] = post_title
    row['Content'] = text
    row['image'] = image