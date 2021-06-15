import re
from loguru import logger

class Content:
    

  def __repr__(self):
    return 'CONTENT IN LOOKER'

  def __init__(self, looker_client):
    self.looker_client = looker_client

  def count_all_errors(self):
    '''Counts errors from Content Validator'''
    '''todo de-duplicate this call to use the validate_content results adding DashErrors and LookErrors'''
    return len(self.looker_client.content_validation().content_with_errors)

  def validate_content(self):
    '''Runs the Content Validator and returns failures'''
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

  def validate_themes(self):
    '''Confirms existing themes are valid'''
    # todo https://company.looker.com:19999/api-docs/index.html#!/4.0/Theme/validate_theme