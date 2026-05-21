from ._anvil_designer import hub_kissTemplate
from anvil import *
import anvil.server
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
    self.refresh_post()


    self.user = anvil.users.get_user()

    self.role = anvil.server.call('get_user_role')
    
    # Hide button
    self.manage_users_button.visible = False
    # Teacher only
    if self.role == "teacher":
      self.manage_users_button.visible = True
  
    # Any code you write here will run before the form opens.

  @handle("New_post_button", "click")
  def New_post_button_click(self, **event_args):
    open_form('add_card') #bring the user to the card adding page
    
  def refresh_post(self):
    # Load existing articles from the Data Table, 
    # and display them in the RepeatingPanel
    # Get current user
    self.user = anvil.users.get_user()

    # Get role once only
    self.role = anvil.server.call('get_user_role')

    # Get posts
    posts = anvil.server.call('get_post')

    # Add role + user info
    self.cards_panel.items = [{'post': row,'role': self.role,'user': self.user}for row in posts]

  @handle("search_bar", "pressed_enter")
  def search_bar_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.search_posts()#the user can either enter the search bar to research the posters

  @handle("research_button", "click")
  def research_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.search_posts()#Or if the user use the research button, it will also research the posters

  def search_posts(self):#serach the posters 
    keyword = self.search_bar.text
    if keyword == "":#Show all posts when the search bar is blank
      self.refresh_post()
      return
    results = anvil.server.call('search_posts', keyword)#else if the search bar is not blank
    self.cards_panel.items = [{'post': row,'role': self.role,'user': self.user}for row in results]

  @handle("search_bar", "change")
  def search_bar_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    #adding live rearching so the user can see all poster
    keyword = self.search_bar.text.strip()
    if keyword == "":
      self.refresh_post()
      return
    results = anvil.server.call(
      'search_posts',
      keyword
    )
    self.cards_panel.items = [{'post': row,'role': self.role,'user': self.user}for row in results]

  @handle("manage_users_button", "click")
  def manage_users_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('manage_users')

  @handle("poster_button", "click")
  def poster_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('hub_kiss')

  

  


