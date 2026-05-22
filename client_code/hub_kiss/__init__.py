from ._anvil_designer import hub_kissTemplate
from anvil import *

import anvil.server
import anvil.users

import anvil.google.auth
import anvil.google.drive
from anvil.google.drive import app_files

import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class hub_kiss(hub_kissTemplate):

  def __init__(self, **properties):

    # Set Form properties
    self.init_components(**properties)

    # Default values
    self.user = None
    self.role = None


  # -------------------------
  # Form show event
  # -------------------------
  @handle("", "show")
  def form_show(self, **event_args):
    # Get current user
    self.user = anvil.users.get_user()

    # Get role
    self.role = anvil.server.call(
      'get_user_role'
    )

    # Hide manage user button
    self.manage_users_button.visible = False

    # Teacher only
    if self.role == "teacher":

      self.manage_users_button.visible = True

    # Load posts
    self.refresh_post()


  # -------------------------
  # Refresh posts
  # -------------------------
  def refresh_post(self):

    # Get posts
    posts = anvil.server.call(
      'get_post'
    )

    # Send role + user + post
    self.cards_panel.items = [

      {
        'post': row,
        'role': self.role,
        'user': self.user
      }

      for row in posts
    ]


  # -------------------------
  # Create new post
  # -------------------------
  @handle(
    "New_post_button",
    "click"
  )
  def New_post_button_click(
    self,
    **event_args
  ):

    open_form(
      'add_card'
    )


  # -------------------------
  # Search button
  # -------------------------
  @handle(
    "research_button",
    "click"
  )
  def research_button_click(
    self,
    **event_args
  ):

    self.search_posts()


  # -------------------------
  # Search enter
  # -------------------------
  @handle(
    "search_bar",
    "pressed_enter"
  )
  def search_bar_pressed_enter(
    self,
    **event_args
  ):

    self.search_posts()


  # -------------------------
  # Live search
  # -------------------------
  @handle(
    "search_bar",
    "change"
  )
  def search_bar_change(
    self,
    **event_args
  ):

    self.search_posts()


  # -------------------------
  # Search system
  # -------------------------
  def search_posts(self):

    keyword = (
      self.search_bar.text
        .strip()
    )

    # Show all posts
    if keyword == "":

      self.refresh_post()
      return

    # Search
    results = anvil.server.call(
      'search_posts',
      keyword
    )

    # Show results
    self.cards_panel.items = [

      {
        'post': row,
        'role': self.role,
        'user': self.user
      }

      for row in results
    ]


  # -------------------------
  # Manage users
  # -------------------------
  @handle(
    "manage_users_button",
    "click"
  )
  def manage_users_button_click(
    self,
    **event_args
  ):

    open_form(
      'manage_users'
    )


  # -------------------------
  # Poster page
  # -------------------------
  @handle(
    "poster_button",
    "click"
  )
  def poster_button_click(
    self,
    **event_args
  ):

    open_form(
      'hub_kiss'
    )


  # -------------------------
  # Logout
  # -------------------------
  @handle(
    "logout_button",
    "click"
  )
  def logout_button_click(
    self,
    **event_args
  ):

    # Confirm logout
    confirm = alert(

      content=
      "Are you sure you want to logout?",

      title="Logout",

      buttons=[

        ("Logout", True),

        ("Cancel", False)

      ]
    )

    # Logout
    if confirm:

      anvil.users.logout()

      open_form(
        'login_page'
      )