from ._anvil_designer import manage_usersTemplate
from anvil import *
import anvil.server


class manage_users(
  manage_usersTemplate
):

  def __init__(
    self,
    **properties
  ):

    self.init_components(
      **properties
    )

    # Load users
    self.refresh_users()


  def refresh_users(self):

    # Get all users
    users = anvil.server.call(
      'get_all_users'
    )

    # Show users
    self.users_panel.items = users


  @handle(
    "back_button",
    "click"
  )
  def back_button_click(
    self,
    **event_args
  ):

    open_form(
      'hub_kiss'
    )