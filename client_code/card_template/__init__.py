from ._anvil_designer import card_templateTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class card_template(card_templateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Any code you write here will run before the form opens.
    # If there is no image,
    # hide image component
    if self.item['image'] is None:
      self.image_1.visible = False
    else:
      self.image_1.visible = True

    #Auto login
    user = anvil.users.get_user()
    if user:
      open_form('hub_kiss')
    else:
      anvil.users.login_with_form()


    #Get user's role
    user = anvil.users.get_user()
    role = anvil.server.call('get_user_role')
    
    # Default:
    # hide buttons
    self.edit_button.visible = False
    self.delete_button.visible = False
    
    # Teacher:
    # can edit everything
    if role == "teacher":
    
      self.edit_button.visible = True
      self.delete_button.visible = True
    
    
    # Student or ambassadors:
    # only own post
    elif self.item['creator'] == user:
      self.edit_button.visible = True
      self.delete_button.visible = True
    
  
  @handle("edit_button", "click")
  def edit_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('edit_card', row=self.item)

  def login_button_click(self, **event_args):
    user = anvil.users.login_with_form()
    if user:
      open_form('hub_kiss')
    
