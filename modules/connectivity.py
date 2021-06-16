from typing import List
from loguru import logger
from looker_sdk.sdk.api40 import methods


class Connectivity:


  def __repr__(self) -> str:
    return 'CONNECTIVITY IN LOOKER'

  def __init__(self, looker_client: methods.Looker40SDK) -> None:
    self.looker_client = looker_client

  def count_all_connections(self) -> int:
    """Gets the number of connections defined.

    Returns:
      The number of database connections set in Looker.
    """
    return len(self.looker_client.all_connections(fields='name'))

  def test_db_connections(self) -> List[str]:
    """Test the connections and returns failures.

    Returns:
      db_errors: The list of errors from database connection tests.
    """
    all_connections = self.looker_client.all_connections(
        fields='name, port, host, dialect(connection_tests, label)'
        )
    db_errors = []

    for connection in all_connections:
      if connection.name not in ('looker', 'looker__ilooker', 
                                'looker__internal__analytics', 'looker_app'):
        if connection.dialect:
          connection_tests = {'tests': connection.dialect.connection_tests}
          for test in connection_tests['tests']:
            try:
              db_validation = self.looker_client.test_connection(connection.name, test)
              for item in db_validation:
                if item.status != 'success':
                  db_errors.append("Database Connection {} Test '{}' returned '{}'".format(
                            connection.name,
                            item.name,
                            item.message)
                            )
                  break
            except Exception as e:
              logger.error('Database Connection test for {} failed due to {}'.format(
                  connection.name, e))
    return db_errors

  def count_all_integrations(self) -> int:
    """Gets the number of integrations set up.

    Returns:
      The number of integrations set up in Looker.
    """
    return len(self.looker_client.all_integrations(fields='id'))

  def test_integrations(self) -> List[str]:
    """Tests the integrations and returns failures.

    Returns:
      integration_errors: The list of errors from integration tests.
    """
    all_integrations = self.looker_client.all_integrations(fields='id, label, enabled')
    integration_errors = []

    for elem in all_integrations:
      if elem.enabled:
        try:
          integration_test = self.looker_client.test_integration(str(elem.id))
          if not integration_test.success:
            integration_errors.append("FAILED - Integration {} connectivity test".format(
                elem.label)
                )
          else:
            integration_errors.append("SUCCESS - Integration {} connectivity test".format(
                elem.label)
                )
        except Exception as e:
          integration_errors.append("Integration {} connectivity test could not run due to {}".format(
              elem.label, e)
              )
      else:
        pass
    return integration_errors

  def count_all_datagroups(self) -> int:
    """Gets the number of datagroups defined.

    Returns:
      The number of datagroups defined in Looker.
    """
    return len(self.looker_client.all_datagroups())

  def test_datagroups(self) -> List[str]:
    """Tests the datagroups and returns failures.

    Returns:
      group_errors:  The list of errors for the Looker Datagroups.
    """
    all_datagroups = self.looker_client.all_datagroups()

    group_errors = [
        "Datagroup \"{}\" on model \"{}\" has this error:\t{}".format(
                                elem.name,
                                elem.model_name,
                                elem.trigger_error)
        for elem in all_datagroups if elem.trigger_error
    ]
    return group_errors