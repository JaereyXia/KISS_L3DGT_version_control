from ._anvil_designer import hub_kissTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users

class hub_kiss(hub_kissTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)



  



  
    # Any code you write here will run before the form opens.

  @handle("Home", "click")
  def Home_click(self, **event_args):
    """This event is called when the button is clicked"""    
    open_form('hub_kiss')#go back to hub

  @handle("New_post_button", "click")
  def New_post_button_click(self, **event_args):
    open_form('card')
    
    
