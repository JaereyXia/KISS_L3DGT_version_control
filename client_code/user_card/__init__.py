from ._anvil_designer import user_cardTemplate
from anvil import *
import anvil.server


class user_card(user_cardTemplate):

  def __init__(self, **properties):

    self.init_components(
      **properties
    )

    # -----------------
    # Dropdown options
    # -----------------

    self.role_dropdown.items = [

      "student",
      "ambassador",
      "teacher"

    ]

    # -----------------
    # Show email
    # -----------------

    self.email_label.text = (
      self.item['user']['email']
    )

    # -----------------
    # Current role
    # -----------------

    self.role_dropdown.selected_value = (
      self.item['role']
    )


  @handle(
    "save_button",
    "click"
  )
  def save_button_click(
    self,
    **event_args
  ):

    # Get selected role
    role = (
      self.role_dropdown
        .selected_value
    )

    # Update role
    anvil.server.call(

      'update_user_role',

      self.item,

      role

    )

    Notification(
      "Role updated"
    ).show()