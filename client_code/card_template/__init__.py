from ._anvil_designer import card_templateTemplate
from anvil import *
import anvil.server


class card_template(card_templateTemplate):

  def __init__(self, **properties):

    self.init_components(**properties)

    # Get data
    post = self.item['post']
    role = self.item['role']
    user = self.item['user']

    # -------------------------
    # Show title/content
    # -------------------------

    self.title_label.text = (
      post['Card_name']
    )

    self.content_label.text = (
      post['Content']
    )


    # -------------------------
    # Image system
    # -------------------------

    # Hide image if empty
    if post['image'] is None:

      self.image_1.visible = False

    else:

      self.image_1.visible = True
      self.image_1.source = (
        post['image']
      )

    # -------------------------
    # Permission system
    # -------------------------

    # Hide buttons by default
    self.edit_button.visible = False
    self.delete_button.visible = False

    # Teacher:
    # full permission
    if role == "teacher":

      self.edit_button.visible = True
      self.delete_button.visible = True

    # Student / committee:
    # own post only
    elif post['creator'] == user:

      self.edit_button.visible = True
      self.delete_button.visible = True


  @handle("edit_button", "click")
  def edit_button_click(
    self,
    **event_args
  ):

    # Open edit form
    open_form(
      'edit_card',
      row=self.item['post']
    )


  @handle("delete_button", "click")
  def delete_button_click(
    self,
    **event_args
  ):

    # Confirm delete
    confirm = alert(
      content=(
        "Are you sure "
        "you want to "
        "delete this post?"
      ),
      title="Delete Post",
      buttons=[
        ("Delete", True),
        ("Cancel", False)
      ]
    )

    if confirm:

      anvil.server.call(
        'delete_post',
        self.item['post']
      )

      Notification(
        "Post deleted"
      ).show()

      open_form('hub_kiss')