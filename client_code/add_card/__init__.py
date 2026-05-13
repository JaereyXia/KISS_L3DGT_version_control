from ._anvil_designer import add_cardTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..card_template import card_template


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
    new_post = {}
    add_card(item = new_post)
    print(new_post)
    
    
    
    """We can now display the ‘card’ Form in our popup by customising the alert using Anvil’s custom popup styles. 
    Set the content property of the alert to an instance of the ‘card’ Form, set the title property to “Add an post”, 
    and set the large property to True:""" 
    alert(
      content=card_template(),
          title="preview",
          large=True,
    )



  
   



    
