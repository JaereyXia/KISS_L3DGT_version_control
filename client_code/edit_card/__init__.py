from ._anvil_designer import edit_cardTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class edit_card(edit_cardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.

    """If the key is true, it allow the post to be send, but if the key is false, 
    it means the user haven't fill in all the context"""
    self.check_key = False

  @handle("back_home_botton", "click")
  def back_home_botton_click(self, **event_args):
    open_form("hub_kiss")

  def clear_inputs(self):
    # Clear our two text boxes
    self.post_title_descriptive.text = ""
    self.text_area_1.text = ""

  def check_blank_post(self):  # this is to check if the poster is fill in or not
    # if any of the text box is blank, the code will send a notification to the user to tell him/her
    if self.post_title_descriptive.text == "":
      Notification(
        "You haven't added a title to this article yet. Please check the title again."
      ).show()
    elif self.text_area_1.text == "":
      Notification(
        "You haven't added a content to this article yet. Please check the content again."
      ).show()
    else:  # else the code will tell the key that the user has fill the post and it's ready to be send.
      self.check_key = True

  @handle("cancel_button", "click")
  def cancer_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    # Add double-checking to ensure users clearly understand that they want to cancel posting.
    save_clicked = alert(
      content="Are you sure to cancel this post?",
      title="Cancel the post",
      large=True,
      buttons=[("Yes", True), ("No", False)],
    )
    if (
      save_clicked
    ):  # if the user is sure and clicked Yes buttom, send him/her back to hub page
      open_form("hub_kiss")

  @handle("save_button", "click")
  def save_button_click(self, **event_args):
    # This method is called when the button is clicked
    post_title = (
      self.post_title_descriptive.text
    )  # Set 'post_title' to the text in the 'self.post_title_descriptive'
    text = self.text_area_1.text  # Set 'text' to the text in the 'text area'
    # pass in post_title, text as arguments
    self.check_blank_post()  # check if the text area or post title is blank
    if self.check_key:  # if the key is true, then it means that the user fill in the post title and post content
      anvil.server.call(
        "add_post", post_title, text
      )  # Set 'feedback' to the text in the 'feedback_box'
      Notification(
        "Post created"
      ).show()  # Show a popup that says 'Feedback submitted!'
      self.clear_inputs()  # Call your 'clear_inputs' method to clear the boxes
