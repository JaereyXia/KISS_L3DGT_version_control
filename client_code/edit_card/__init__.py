from ._anvil_designer import edit_cardTemplate
from anvil import *
import anvil.server


class edit_card(edit_cardTemplate):

  def __init__(
    self,
    row=None,
    **properties
  ):

    # Initialize form
    self.init_components(**properties)

    # Save row
    self.row = row

    # Default image
    self.new_image = None

    # Load existing data
    if self.row:

      self.post_title_descriptive.text = (
        self.row['Card_name']
      )

      self.text_area_1.text = (
        self.row['Content']
      )

      self.post_image.source = (
        self.row['image']
      )

    # Validation key
    self.check_key = False


  @handle("image_uploader", "change")
  def image_uploader_change(
    self,
    file,
    **event_args
  ):

    # Save uploaded image
    self.new_image = file

    # Show preview
    self.post_image.source = file


  @handle("back_home_botton", "click")
  def back_home_botton_click(
    self,
    **event_args
  ):

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

    # Allow save
    else:

      self.check_key = True


  @handle("cancel_button", "click")
  def cancer_button_click(
    self,
    **event_args
  ):

    # Double-check cancel
    save_clicked = alert(
      content="Are you sure to cancel this edit?",
      title="Cancel Edit",
      large=True,
      buttons=[
        ("Yes", True),
        ("No", False)
      ]
    )

    if save_clicked:

      open_form("hub_kiss")


  @handle("save_button", "click")
  def save_button_click(
    self,
    **event_args
  ):

    # Get title
    post_title = (
      self.post_title_descriptive.text
    )

    # Get content
    text = self.text_area_1.text

    # Check blanks
    self.check_blank_post()

    # Passed validation
    if self.check_key:

      # Keep old image
      # if user didn't upload new one
      image = getattr(
        self,
        "new_image",
        self.row['image']
      )

      # Update post
      anvil.server.call(
        "update_post",
        self.row,
        post_title,
        text,
        image
      )

      Notification(
        "Post updated"
      ).show()

      # Return home
      open_form('hub_kiss')