from ._anvil_designer import edit_cardTemplate
from anvil import *
import anvil.server
import anvil.users


class edit_card(edit_cardTemplate):

  def __init__(self, row=None, **properties):

    # Initialize form
    self.init_components(**properties)

    # Get current user's role
    self.role = anvil.server.call('get_user_role')

    # Hide Manage Users button
    self.manage_users_button.visible = False

    # Teacher only
    if self.role == "teacher":
      self.manage_users_button.visible = True

    # Save selected row
    self.row = row

    # Store uploaded image
    self.new_image = None

    # Load existing post data
    if self.row:

      # Load title
      self.post_title_descriptive.text = self.row['Card_name']

      # Load content
      self.text_area_1.text = self.row['Content']

      # Load image
      self.post_image.source = self.row['image']

    # Validation key
    self.check_key = False


  @handle("image_uploader", "change")
  def image_uploader_change(self, file, **event_args):

    # Save new uploaded image
    self.new_image = file

    # Show preview image
    self.post_image.source = file


  @handle("back_home_botton", "click")
  def back_home_botton_click(self, **event_args):

    # Return homepage
    open_form("hub_kiss")


  def check_blank_post(self):

    # Reset validation
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

    # Passed validation
    else:

      self.check_key = True


  @handle("cancel_button", "click")
  def cancel_button_click(self, **event_args):

    # Ask user to confirm cancel
    cancel_clicked = alert(
      content="Are you sure you want to cancel this edit?",
      title="Cancel Edit",
      large=True,
      buttons=[
        ("Yes", True),
        ("No", False)
      ]
    )

    # Return homepage
    if cancel_clicked:
      open_form("hub_kiss")


  @handle("save_button", "click")
  def save_button_click(self, **event_args):

    # Get updated title
    post_title = self.post_title_descriptive.text

    # Get updated content
    text = self.text_area_1.text

    # Check blank fields
    self.check_blank_post()

    # Continue if validation passed
    if self.check_key:

      # Keep old image if
      # user did not upload new one
      image = self.new_image or self.row['image']

      # Update database row
      anvil.server.call(
        "update_post",
        self.row,
        post_title,
        text,
        image
      )

      # Success message
      Notification(
        "Post updated"
      ).show()

      # Return homepage
      open_form('hub_kiss')


  @handle("poster_button", "click")
  def poster_button_click(self, **event_args):

    # Return homepage
    open_form('hub_kiss')


  @handle("manage_users_button", "click")
  def manage_users_button_click(self, **event_args):

    # Open Manage Users page
    open_form('manage_users')


  @handle("logout_button", "click")
  def logout_button_click(self, **event_args):

    # Confirm logout
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

      # Return login page
      open_form('login_page')