from ._anvil_designer import add_cardTemplate
from anvil import *
import anvil.server
import anvil.users


class add_card(add_cardTemplate):

  def __init__(self, **properties):

    # Initialize form components
    self.init_components(**properties)

    # Get current user's role
    # This is used to decide whether
    # the Manage Users button is visible
    self.role = anvil.server.call('get_user_role')

    # Hide Manage Users button by default
    self.manage_users_button.visible = False

    # Only teacher can access Manage Users
    if self.role == "teacher":
      self.manage_users_button.visible = True

    # Boolean key to check
    # whether the post passes validation
    self.check_key = False

    # Default image is None
    # until user uploads one
    self.image = None


  @handle("back_home_botton", "click")
  def back_home_botton_click(self, **event_args):

    # Return user to homepage
    open_form('hub_kiss')


  def clear_inputs(self):

    # Clear title textbox
    self.post_title_descriptive.text = ""

    # Clear content textbox
    self.text_area_1.text = ""

    # Remove image preview
    self.post_image.source = None

    # Reset image variable
    self.image = None


  def check_blank_post(self):

    # Reset validation key
    # every time function runs
    self.check_key = False

    # Check if title is empty
    if self.post_title_descriptive.text == "":

      Notification(
        "You haven't added a title yet."
      ).show()

    # Check if content is empty
    elif self.text_area_1.text == "":

      Notification(
        "You haven't added content yet."
      ).show()

    # If both title and content exist,
    # allow the post to be submitted
    else:
      self.check_key = True


  @handle("cancel_button", "click")
  def cancel_button_click(self, **event_args):

    # Ask user to confirm cancelling
    cancel_clicked = alert(
      content="Are you sure you want to cancel this post?",
      title="Cancel Post",
      large=True,
      buttons=[
        ("Yes", True),
        ("No", False)
      ]
    )

    # Return to homepage if confirmed
    if cancel_clicked:
      open_form('hub_kiss')


  @handle("save_button", "click")
  def save_button_click(self, **event_args):

    # Get post title from textbox
    post_title = self.post_title_descriptive.text

    # Get post content
    text = self.text_area_1.text

    # Get uploaded image
    image = self.image

    # Check if required fields are filled
    self.check_blank_post()

    # Only save if validation passes
    if self.check_key:

      # Call server function
      # to add post into database
      anvil.server.call(
        'add_post',
        post_title,
        text,
        image
      )

      # Show success notification
      Notification(
        "Post created"
      ).show()

      # Return to homepage
      open_form('hub_kiss')


  @handle("image_uploader", "change")
  def image_uploader_change(self, file, **event_args):

    # Save uploaded image
    self.image = file

    # Show image preview
    self.post_image.source = file


  @handle("poster_button", "click")
  def poster_button_click(self, **event_args):

    # Return to homepage
    open_form('hub_kiss')


  @handle("manage_users_button", "click")
  def manage_users_button_click(self, **event_args):

    # Open Manage Users page
    # Only visible to teacher
    open_form('manage_users')


  @handle("logout_button", "click")
  def logout_button_click(self, **event_args):

    # Ask user to confirm logout
    confirm = alert(
      content="Are you sure you want to logout?",
      title="Logout",
      buttons=[
        ("Logout", True),
        ("Cancel", False)
      ]
    )

    # Logout if confirmed
    if confirm:

      # Logout current user
      anvil.users.logout()

      # Return to login page
      open_form('login_page')