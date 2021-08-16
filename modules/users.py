from looker_sdk.sdk.api40 import methods
from looker_sdk.sdk.api40 import models
from typing import List

class Users:
    
  def __repr__(self) -> str:
    return 'USERS IN LOOKER'

  def __init__(self, looker_client: methods.Looker40SDK):
    self.looker_client = looker_client

  def validate_api_creds(self) -> bool:
    """Ensures the API credentials tie to an Admin user.

    Confirms the user set for Themis has appropriate powers in Looker
    to retrieve all the information from the system. 

	  Returns:
      A boolean value representing the 'Admin' value in list of roles.
    """
    api_user = self.looker_client.me()
    all_roles = [
        self.looker_client.role(role_id).name.lower() == "admin" 
        for role_id in api_user.role_ids
    ]
    return True in all_roles

  def count_all_users(self) -> int:
    """Retrieves number of users in the Looker instance.

	  Returns:
      The number of users in the Looker instance.
    """
    return len(self.looker_client.all_users(fields='id'))

  def get_users_issue(self) -> List[str]:
    """Retrieves the locked out users in the Looker instance.

	  Returns:
      user_results: The list with information on disabled and locked out users.
    """
    all_users = self.looker_client.all_users(fields='id, is_disabled')
    disabled_users = [ user for user in all_users if user.is_disabled ]

    user_results = ["Disabled Looker users: {}".format(len(disabled_users))]
    locked_out = self.looker_client.all_user_login_lockouts()
    user_results.append("Locked Out Looker users: {}".format(len(locked_out)))
    return user_results

  def get_inactive_users(self) -> int:
    """Returns users without login data for past 90 days.

	  Returns:
      len(inactive_users): The number of inactive users in Looker.
    """
    body = models.WriteQuery(
    model = "system__activity",
    view = "user",
    fields = [
        "user.id",
        "user.name"
    ],
    filters = {
        "user_facts.is_looker_employee": "no",
        "user.is_disabled": "no"
    },
    filter_expression = {
        "diff_days(${user_facts.last_api_login_date}, now()) > 90 OR diff_days(${user_facts.last_ui_login_date}, now()) > 90"
    },
    sorts = [
        "user.id"
    ],
    limit = "500"
    )
    users_query = self.looker_client.create_query(body)
    inactive_users = self.looker_client.run_query(users_query.id, result_format='json')
    return len(inactive_users)