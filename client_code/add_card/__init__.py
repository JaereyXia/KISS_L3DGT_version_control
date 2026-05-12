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

  @handle("outlined_button_1", "click")
  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('hub_kiss')

  @handle("outlined_button_2", "click")
  def outlined_button_2_click(self, **event_args):
    #This method is called when the button is clicked
    """We can now display the ‘card’ Form in our popup by customising the alert using Anvil’s custom popup styles. 
    Set the content property of the alert to an instance of the ‘card’ Form, set the title property to “Add an article”, 
    and set the large property to True:"""
    alert(
      content=add_card(),
          title="Add poster",
          large=True,
    )



    
