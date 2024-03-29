import re
from typing import Tuple, List
from loguru import logger

class Content:
    

  def __repr__(self) -> str:
    return 'CONTENT IN LOOKER'

  def __init__(self, looker_client) -> None:
    self.looker_client = looker_client

  def count_all_errors(self) -> int:
    """Counts errors from Looker Content Validator.

    Returns:
      The number of erring content in Looker.
    """
    return len(self.looker_client.content_validation().content_with_errors)

  def validate_content(self) -> Tuple[List[str], List[str], int, int]:
    """Runs the Content Validator and returns failures.

    Returns:
      looks_error: The list of unique errors for the Looks.
      dash_errors: The list of unique errors for the Dashboards.
      total_look_errors: The total count of errors for Looks.
      total_dash_errors: The total count of errors for Dashboards.
    """
    error = self.looker_client.content_validation().content_with_errors
    looks_error, dash_errors = [], []
    for i in range(0, len(error)):
      error_msg = re.sub(r'\[ContentValidationError\(message=', '', str(error[i].errors))
      error_msg = re.sub(r'\, field_name=.*', '', error_msg)
      if error[i].look:
        looks_error.append("Look {} titled \"{}\" has this error: {}".format(
            error[i].look.id, error[i].look.title, error_msg)
            )
      elif error[i].dashboard:
        dash_errors.append("Dashboard {} titled \"{}\" has this error: {}".format(
            error[i].dashboard.id, error[i].dashboard.title, error_msg)
            )
      else:
        logger.warning('Did not account for content {}'.format(error[i]))

    looks_error = list(set(looks_error)) # set to remove duplicates
    total_look_errors = len(looks_error)
    dash_errors = list(set(dash_errors))
    total_dash_errors = len(dash_errors)
    return looks_error, dash_errors, total_look_errors, total_dash_errors

  def validate_themes(self) -> None:
    '''Confirms existing themes are valid'''
    # todo https://company.looker.com:19999/api-docs/index.html#!/4.0/Theme/validate_theme
    # 1. SDK all_themes()
    # 2. parse response into list of themes
    # 3. for each theme, call SDK validate_theme(body)