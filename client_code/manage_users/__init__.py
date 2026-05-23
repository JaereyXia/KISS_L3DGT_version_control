from ._anvil_designer import manage_usersTemplate
from anvil import *
import anvil.server
import anvil.users


class manage_users(manage_usersTemplate):

  def __init__(self, **properties):

    # Initialize form
    self.init_components(**properties)

    # Get current role
    self.role = anvil.server.call(
      'get_user_role'
    )

    # Security check
    # Only teacher can access
    if self.role != "teacher":

      Notification(
        "No permission."
      ).show()

      open_form('hub_kiss')
      return

    # Show manage button
    self.manage_users_button.visible = True

    # Load all users
    self.refresh_users()


  # -------------------------
  # Refresh users
  # -------------------------
  def refresh_users(self):

    users = anvil.server.call(
      'get_all_users'
    )

    self.users_panel.items = users


  # -------------------------
  # Back button
  # -------------------------
  @handle("back_button", "click")
  def back_button_click(self, **event_args):

    open_form('hub_kiss')


  # -------------------------
  # Home button
  # -------------------------
  @handle("button_1", "click")
  def poster_button_click(self, **event_args):

    open_form('hub_kiss')


  # -------------------------
  # Manage users
  # -------------------------
  @handle("manage_users_button", "click")
  def manage_users_button_click(self, **event_args):

    open_form('manage_users')


  # -------------------------
  # Logout
  # -------------------------
  @handle("logout_button", "click")
  def logout_button_click(self, **event_args):

    confirm = alert(
      content="Are you sure you want to logout?",
      title="Logout",
      buttons=[
        ("Logout", True),
        ("Cancel", False)
      ]
    )

    if confirm:

      anvil.users.logout()

      open_form('login_page')