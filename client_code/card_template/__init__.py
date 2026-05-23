from ._anvil_designer import card_templateTemplate
from anvil import *
import anvil.server


class card_template(card_templateTemplate):

  def __init__(self, **properties):

    # Initialize form components
    self.init_components(**properties)
    

    # Get current post data
    post = self.item['post']

    # Get current user role
    role = self.item['role']

    # Get current logged in user
    user = self.item['user']
    
    # -------------------------
    # Display post information
    # -------------------------

    # Show post title
    self.title_label.text = post['Card_name']

    # Show post content
    self.content_label.text = post['Content']


    # -------------------------
    # Image system
    # -------------------------

    # Hide image area if
    # there is no uploaded image
    if post['image'] is None:

      self.image_1.visible = False

    else:

      # Show image
      self.image_1.visible = True

      # Load image from database
      self.image_1.source = post['image']


    # -------------------------
    # Permission system
    # -------------------------

    # Hide edit/delete buttons
    # by default
    self.edit_button.visible = False
    self.delete_button.visible = False

    # Teacher can edit/delete
    # all posts
    if role == "teacher":

      self.edit_button.visible = True
      self.delete_button.visible = True

    # Students / ambassadors
    # can only edit their own post
    elif post['creator'] == user:

      self.edit_button.visible = True
      self.delete_button.visible = True


  @handle("edit_button", "click")
  def edit_button_click(self, **event_args):

    # Open edit page
    # Pass selected post row
    open_form(
      'edit_card',
      row=self.item['post']
    )


  @handle("delete_button", "click")
  def delete_button_click(self, **event_args):

    # Ask user to confirm delete
    confirm = alert(
      content="Are you sure you want to delete this post?",
      title="Delete Post",
      buttons=[
        ("Delete", True),
        ("Cancel", False)
      ]
    )

    # Delete if confirmed
    if confirm:

      # Call server function
      # to delete database row
      anvil.server.call(
        'delete_post',
        self.item['post']
      )

      # Success message
      Notification(
        "Post deleted"
      ).show()

      # Refresh homepage
      open_form('hub_kiss')