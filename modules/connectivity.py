import re
from loguru import logger
# import threading

class Connectivity:


  def __repr__(self):
    return 'CONNECTIVITY IN LOOKER'

  def __init__(self, looker_client):
    self.looker_client = looker_client

  def count_all_connections(self):
    '''Gets the number of connections defined'''
    # todo confirm if this include internal connections and remove looker connection
    return len(self.looker_client.all_connections(fields='id'))

  def test_db_connections(self):
    '''Test the connections and returns failures'''
    # todo if _connect_ fails no need to run other tests + add threading for connections
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
            except Exception as e:
              logger.error('Database Connection test for {} failed due to {}'.format(
                  connection.name, e))
    return db_errors

  def count_all_integrations(self):
    '''Gets the number of integrations set up'''
    return len(self.looker_client.all_integrations(fields='id'))

  def test_integrations(self):
    '''Tests the integrations and returns failures'''
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
        # integration_errors.append("Integration {} not enabled.".format(elem.label))
        pass
    return integration_errors

  def count_all_datagroups(self):
    '''Gets the number of datagroups defined'''
    return len(self.looker_client.all_datagroups())

  def test_datagroups(self):
    '''Tests the datagroups and returns failures'''
    all_datagroups = self.looker_client.all_datagroups()
    group_errors = []
    for elem in all_datagroups:
      if elem.trigger_error:
        group_errors.append("Datagroup \"{}\" on model \"{}\" has this error:\t{}".format(
                                elem.name,
                                elem.model_name,
                                elem.trigger_error)
                                )
    return group_errors