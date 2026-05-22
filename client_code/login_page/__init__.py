from ._anvil_designer import login_pageTemplate
from anvil import *
import anvil.users
import anvil.server


class login_page(
  login_pageTemplate
):

  def __init__(
    self,
    **properties
  ):

    self.init_components(
      **properties
    )

    self.login()


  def login(self):

    # Already logged in
    user = (
      anvil.users.get_user()
    )

    # Go homepage directly
    if user:

      open_form(
        'hub_kiss'
      )

      return

    # Open login/signup form
    user = (
      anvil.users
        .login_with_form()
    )

    # Login success
    if user:

      # Create profile
      anvil.server.call(
        'ensure_user_profile'
      )

      # Go homepage
      open_form(
        'hub_kiss'
      )