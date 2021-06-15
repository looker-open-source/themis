import json
from looker_sdk.sdk.api40 import methods
from looker_sdk.sdk.api40 import methods
from typing import Tuple

class Schedules:
    
  def __repr__(self) -> str:
    return 'SCHEDULES IN LOOKER'

  def __init__(self, looker_client: methods.Looker40SDK) -> None:
    self.looker_client = looker_client

  def count_all_schedules(self) -> int:
    '''Counts number of schedules'''
    return len(self.looker_client.all_scheduled_plans(fields='id', all_users=True))

  def get_failed_schedules(self) -> Tuple[str, int]:
    '''Finds failed email schedules'''
    body = models.WriteQuery(
        model = "system__activity",
        view = "scheduled_plan",
        fields = [
            "scheduled_job.status",
            "scheduled_plan.id",
            "scheduled_job.name",
            "scheduled_plan_destination.format",
            "scheduled_plan_destination.type",
            "look.id",
            "dashboard.id"
        ],
        filters = {
            "scheduled_plan.run_once": "no",
            "scheduled_job.status": "failure",
            "scheduled_job.created_date": "this week"
        },
        sorts = ["scheduled_job.created_date", "scheduled_plan.id desc"],
        limit = "500"
    )
    schedules_query = self.looker_client.create_query(body)
    failed_schedules = self.looker_client.run_query(schedules_query.id, result_format='json')
    cleaned_errors = []
    for elem in json.loads(failed_schedules):
      cleaned_errors.append("Schedule \'{}\' failed to send to {}".format(
                            elem['scheduled_job.name'], 
                            elem['scheduled_plan_destination.type'])
                            )
    if failed_schedules:
      cleaned_errors = list(set(cleaned_errors)) # set to remove duplicates
      return cleaned_errors, len(json.loads(failed_schedules))
    else:
      return None,0

  def get_pdts_status(self) -> Tuple[str, int]:
    '''Finds PDTs with issues'''
    body = models.WriteQuery(
        model = "system__activity",
        view = "pdt_event_log",
        fields = ["pdt_event_log.view_name", "pdt_event_log.connection"],
        filters = {"pdt_event_log.action": "%error%", 
                   "pdt_event_log.created_time": "24 hours"},
        sorts = ["pdt_event_log.connection"],
        limit = "5000"
    )
    failed_pdts = self.looker_client.create_query(body)
    failed_pdts_list = self.looker_client.run_query(failed_pdts.id, result_format='json')
    cleaned_errors = []
    for elem in json.loads(failed_pdts_list):
      cleaned_errors.append("PDT \'{}\' failed on connection: {}".format(
                            elem['pdt_event_log.view_name'], 
                            elem['pdt_event_log.connection'])
                            )
    if failed_pdts_list:
      cleaned_errors = list(set(cleaned_errors)) # set to remove duplicates
      return cleaned_errors, len(json.loads(failed_pdts_list))
    else:
      return None,0

  def get_pdts_buildtimes(self) -> Tuple[int, int, int]: 
    '''Finds PDTs Build Times'''
    body = models.WriteQuery(
        model = "system__activity",
        view = "pdt_builds",
        fields = ["pdt_builds.view_name", "pdt_builds.connection", "pdt_builds.average_build_time_minutes"],
        filters = {
            "pdt_builds.start_date": "24 hours",
            "pdt_builds.status": "done"
        },
        sorts = [
            "pdt_builds.average_build_time_minutes desc"
        ],
        limit = "500",
        dynamic_fields = '[{\"table_calculation\":\"build_less_30\",\"label\":\"build_less_30\",\"expression\":\"sum(if(${pdt_builds.average_build_time_minutes} < 30 AND NOT is_null(${pdt_builds.average_build_time_minutes}),  1, 0))\",\"value_format\":null,\"value_format_name\":null,\"_kind_hint\":\"measure\",\"_type_hint\":\"number\"},{\"table_calculation\":\"build_30_60\",\"label\":\"build_30_60\",\"expression\":\"sum(if(${pdt_builds.average_build_time_minutes} >= 30 AND ${pdt_builds.average_build_time_minutes}<60,\\n  1, 0))\",\"value_format\":null,\"value_format_name\":null,\"_kind_hint\":\"measure\",\"_type_hint\":\"number\"},{\"table_calculation\":\"build_more_60\",\"label\":\"build_more_60\",\"expression\":\"sum(if(${pdt_builds.average_build_time_minutes} >=60,\\n  1, 0))\",\"value_format\":null,\"value_format_name\":null,\"_kind_hint\":\"measure\",\"_type_hint\":\"number\"}]'
    )
    pdt_build_times_query = self.looker_client.create_query(body)
    pdt_build_times = self.looker_client.run_query(pdt_build_times_query.id, result_format='json')
    build_less_30 = json.loads(pdt_build_times)[0]['build_less_30']
    build_30_60 = json.loads(pdt_build_times)[0]['build_30_60'] 
    build_more_60 = json.loads(pdt_build_times)[0]['build_more_60']
    return int(build_less_30 or 0), int(build_30_60 or 0), int(build_more_60 or 0)