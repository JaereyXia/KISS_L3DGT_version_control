import anvil.server
import anvil.users
import anvil.tables as tables
from anvil.tables import app_tables
from datetime import datetime
import uuid


# -------------------------
# Create post
# -------------------------
@anvil.server.callable
def add_post(
  post_title,
  text,
  image
):

  user = anvil.users.get_user()

  app_tables.cards.add_row(

    Card_name=post_title,
    Content=text,
    Created=datetime.now(),
    image=image,

    # Unique ID
    post_id=str(
      uuid.uuid4()
    ),

    # Save creator
    creator=user
  )


# -------------------------
# Get posts
# -------------------------
@anvil.server.callable
def get_post():

  return app_tables.cards.search(
    tables.order_by(
      "Created",
      ascending=False
    )
  )


# -------------------------
# Search posts
# -------------------------
@anvil.server.callable
def search_posts(keyword):

  import difflib

  keywords = (
    keyword.lower()
      .split()
  )

  results = []

  for row in (
    app_tables.cards.search()
  ):

    title = (
      row['Card_name']
      or ""
    ).lower()

    content = (
      row['Content']
      or ""
    ).lower()

    score = 0

    for word in keywords:

      if word in title:
        score += 5

      if word in content:
        score += 3

      for t_word in (
        title.split()
      ):

        similarity = (
          difflib
            .SequenceMatcher(
              None,
              word,
              t_word
            )
            .ratio()
        )

        if similarity > 0.75:
          score += 3

      for c_word in (
        content.split()
      ):

        similarity = (
          difflib
            .SequenceMatcher(
              None,
              word,
              c_word
            )
            .ratio()
        )

        if similarity > 0.75:
          score += 1

    if score > 0:
      results.append(
        (score, row)
      )

  results.sort(
    reverse=True,
    key=lambda x: x[0]
  )

  return [
    row
    for score, row
    in results
  ]


# -------------------------
# Get user role
# -------------------------
@anvil.server.callable
def get_user_role():

  user = (
    anvil.users.get_user()
  )

  if not user:
    return None

  profile = (
    app_tables.profiles.get(
      user=user
    )
  )

  if not profile:
    return "student"

  return profile['role']


# -------------------------
# Update post
# -------------------------
@anvil.server.callable
def update_post(
  row,
  post_title,
  text,
  image
):

  user = (
    anvil.users.get_user()
  )

  profile = (
    app_tables.profiles.get(
      user=user
    )
  )

  role = (
    profile['role']
  )

  is_owner = (
    row['creator']
    == user
  )

  is_teacher = (
    role == "teacher"
  )

  if not (
    is_owner
    or is_teacher
  ):

    raise Exception(
      "No permission."
    )

  row['Card_name'] = (
    post_title
  )

  row['Content'] = (
    text
  )

  row['image'] = image


# -------------------------
# Delete post
# -------------------------
@anvil.server.callable
def delete_post(row):

  user = (
    anvil.users.get_user()
  )

  profile = (
    app_tables.profiles.get(
      user=user
    )
  )

  role = (
    profile['role']
  )

  is_owner = (
    row['creator']
    == user
  )

  is_teacher = (
    role == "teacher"
  )

  if not (
    is_owner
    or is_teacher
  ):

    raise Exception(
      "No permission."
    )

  row.delete()

# -------------------------
# Get all users
# Teacher only
# -------------------------
@anvil.server.callable
def get_all_users():

  # Get current user
  user = anvil.users.get_user()

  # Get current profile
  profile = app_tables.profiles.get(
    user=user
  )

  # No profile
  if not profile:
    raise Exception(
      "No permission."
    )

  # Only teacher
  if profile['role'] != "teacher":
    raise Exception(
      "Teacher access only."
    )

  # Return all profiles
  return app_tables.profiles.search()


# -------------------------
# Update user role
# Teacher only
# -------------------------
@anvil.server.callable
def update_user_role(
  profile_row,
  new_role
):

  # Get current user
  user = anvil.users.get_user()

  # Get profile
  profile = app_tables.profiles.get(
    user=user
  )

  # Teacher only
  if profile['role'] != "teacher":

    raise Exception(
      "No permission."
    )

  # Update role
  profile_row['role'] = new_role