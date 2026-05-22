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

    # Auto login
    self.login()


  def login(self):

    # Open login/signup form
    user = (
      anvil.users
        .login_with_form()
    )

    # Success login
    if user:
      # Ensure profile exists
      anvil.server.call('ensure_user_profile')

      # Go homepage
      open_form(
        'hub_kiss'
      )