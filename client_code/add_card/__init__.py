from ._anvil_designer import add_cardTemplate
from anvil import *
import anvil.server
import anvil.users


class add_card(add_cardTemplate):

  def __init__(self, **properties):

    # Initialize form
    self.init_components(**properties)
    #get user role for premission
    self.role = anvil.server.call('get_user_role')
    # Hide button
    self.manage_users_button.visible = False
    # Teacher only
    if self.role == "teacher":
      self.manage_users_button.visible = True
    
    # If key is True,
    # user can submit post
    self.check_key = False

    # Default image
    self.image = None


  @handle("back_home_botton", "click")
  def back_home_botton_click(self, **event_args):

    # Return to home page
    open_form('hub_kiss')


  def clear_inputs(self):

    # Clear all input boxes
    self.post_title_descriptive.text = ""
    self.text_area_1.text = ""

    # Clear image
    self.post_image.source = None
    self.image = None


  def check_blank_post(self):

    # Reset key every time
    self.check_key = False

    # Check title
    if self.post_title_descriptive.text == "":

      Notification(
        "You haven't added a title yet."
      ).show()

    # Check content
    elif self.text_area_1.text == "":

      Notification(
        "You haven't added content yet."
      ).show()

    # Allow save
    else:

      self.check_key = True


  @handle("cancel_button", "click")
  def cancer_button_click(self, **event_args):

    # Double confirmation
    save_clicked = alert(
      content="Are you sure to cancel this post?",
      title="Cancel Post",
      large=True,
      buttons=[
        ("Yes", True),
        ("No", False)
      ]
    )

    # Return home
    if save_clicked:

      open_form('hub_kiss')


  @handle("save_button", "click")
  def save_button_click(self, **event_args):

    # Get title
    post_title = (
      self.post_title_descriptive.text
    )

    # Get content
    text = self.text_area_1.text

    # Get image
    image = self.image

    # Check blank inputs
    self.check_blank_post()

    # If passed validation
    if self.check_key:

      # Save post
      anvil.server.call(
        'add_post',
        post_title,
        text,
        image
      )

      Notification(
        "Post created"
      ).show()

      # Return to homepage
      open_form('hub_kiss')


  @handle("image_uploader", "change")
  def image_uploader_change(
    self,
    file,
    **event_args
  ):

    # Save image
    self.image = file

    # Preview image
    self.post_image.source = file

  @handle("poster_button", "click")
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
