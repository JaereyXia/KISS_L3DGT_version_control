from ._anvil_designer import manage_usersTemplate
from anvil import *
import anvil.server


class manage_users(manage_usersTemplate):
  def __init__(self,**properties):
    self.init_components(**properties)
    # Load users
    self.refresh_users()

    self.role = anvil.server.call('get_user_role')
    # Hide button
    self.manage_users_button.visible = False
    # Teacher only
    if self.role == "teacher":
      self.manage_users_button.visible = True

  def refresh_users(self):
    # Get all users
    users = anvil.server.call('get_all_users')

    # Show users
    self.users_panel.items = users


  @handle("back_button","click")
  def back_button_click(
    self,
    **event_args
  ):

    open_form(
      'hub_kiss'
    )

  @handle("button_1", "click")
  def poster_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('hub_kiss')

  @handle("manage_users_button", "click")
  def manage_users_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('manage_users')

  @handle("logout_button", "click")
  def logout_button_click(self,**event_args):

    # Confirm logout
    confirm = alert(
      content= "Are you sure you want to logout?",

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
