from ._anvil_designer import add_cardTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables



class add_card(add_cardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  @handle("back_home_botton", "click")
  def back_home_botton_click(self, **event_args):
    open_form('hub_kiss')

  @handle("cancel_button", "click")
  def cancer_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('hub_kiss')

  @handle("save_button", "click")
  def save_button_click(self, **event_args):
    #This method is called when the button is clicked
    post_title = self.post_title_descriptive # Set 'post_title' to the text in the 'self.post_title_descriptive'
    text = self.text_area_1 # Set 'text' to the text in the 'text area'
    # pass in post_title, text as arguments
    self.check_blank_feedback_form()# check if the text area or post title is blank
    if self.key:#if the key is true, then it means that the user fill in the post title and post content
      anvil.server.call('add_feedback', post_title, text) # Set 'feedback' to the text in the 'feedback_box'
      Notification("Post created").show() # Show a popup that says 'Feedback submitted!'


  
    self.clear_inputs() # Call your 'clear_inputs' method to clear the boxes

    
    



  
   



    
