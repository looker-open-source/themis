import os, os.path
from requests.exceptions import ReadTimeout
from loguru import logger
import setup

# modules calling the Looker API to get results
from modules.general import *
from modules.users import Users
from modules.projects import Projects
from modules.content import Content
from modules.schedules import Schedules
from modules.performance import Performance
from modules.connectivity import Connectivity

# modules putting the info together for delivery
from modules.email_content import *
from modules.send_email import send_report_out


# check if deployment uses the .ini file
if path.exists("looker.ini"): 
    looker_client = setup.configure_sdk()
    api_user = Users(looker_client)
    logger.info("Found looker.ini file in the directory.")
# use environment variable instead 
else:
    try:
        LOOKERSDK_API_VERSION = 4.0 # enforcing API 4.0 to access new endpoints when released
        LOOKERSDK_BASE_URL = os.environ.get('LOOKERSDK_BASE_URL')
        LOOKERSDK_CLIENT_ID = os.environ.get('LOOKERSDK_CLIENT_ID')
        LOOKERSDK_CLIENT_SECRET = os.environ.get('LOOKERSDK_CLIENT_SECRET')
        looker_client = setup.configure_sdk()
        api_user = Users(looker_client)
        logger.info("Found Looker ENV VAR in the system.")
    except Exception as e: 
        logger.error('Missing Environment Variables {}'.format(e))

if not api_user.validate_api_creds():
    logger.error('Ensure API credentials have Admin role.')
    exit(0)


looker_version = get_looker_version(looker_client)
looker_url = get_looker_instance()
logger.info('Checking instance: {}'.format(looker_url))

# USERS
all_users = api_user.count_all_users()
user_issue_details = api_user.get_users_issue()
logger.info('Checked: {}'.format(Users.__repr__(api_user)))
####################################################################

# PROJECTS
my_project = Projects(looker_client)
count_all_projects = my_project.count_all_projects()

all_projects = my_project.all_projects()  # to reuse throughout code
logger.info('Checked: {}'.format(Projects.__repr__(my_project)))
####################################################################

# CONTENT
my_content = Content(looker_client)
count_content_errors = my_content.count_all_errors()

content_errors = my_content.validate_content()
total_look_errors = content_errors[2]
look_errors = format_output(content_errors[0])

total_dash_errors = content_errors[3]
dashboards_errors = format_output(content_errors[1])
logger.info('Checked: {}'.format(Content.__repr__(my_content)))
####################################################################

# SCHEDULES
my_schedule = Schedules(looker_client)
count_all_schedules = my_schedule.count_all_schedules()
count_schedule_errors = my_schedule.get_failed_schedules()[1]
all_schedule_errors = my_schedule.get_failed_schedules()[0]
schedule_errors = format_output(all_schedule_errors)

all_pdt_errors = my_schedule.get_pdts_status()
count_pdt_errors = all_pdt_errors[1]
pdt_errors = format_output(all_pdt_errors[0])

pdt_build_times = my_schedule.get_pdts_buildtimes()
logger.info('Checked: {}'.format(Schedules.__repr__(my_schedule)))
####################################################################

# PERFORMANCE
my_performance = Performance(looker_client)
# no row detail in report to not expose user.id or user.name
test_unlimited_queries = my_performance.unlimited_downloads() 
unlimited_queries = test_unlimited_queries[0]
report_url = test_unlimited_queries[1]

is_instance_clustered = my_performance.check_if_clustered()
list_nodes = my_performance.nodes_matching() if is_instance_clustered else [None]
    
logger.info('Checked: {}'.format(Performance.__repr__(my_performance)))
####################################################################

# CONNECTIVITY
my_connective = Connectivity(looker_client)

count_connections = my_connective.count_all_connections()
all_connection_errors = my_connective.test_db_connections()
connection_errors = format_output(all_connection_errors)

count_integrations = my_connective.count_all_integrations()
all_integration_errors = my_connective.test_integrations()
integration_errors = format_output(all_integration_errors)

count_datagroups = my_connective.count_all_datagroups()
all_datagroup_errors = my_connective.test_datagroups()
datagroup_errors = format_output(all_datagroup_errors)
logger.info('Checked: {}'.format(Connectivity.__repr__(my_connective)))
####################################################################

# create the attachment details for the various items checked (summary + details)
email_attachment(looker_url = looker_url, looker_version = looker_version,
                 total_users = all_users, user_details = user_issue_details,
                 total_projects = count_all_projects,
                 total_erring_content = count_content_errors,
                 total_look_errors = total_look_errors, 
                 look_errors = look_errors,
                 total_dash_errors = total_dash_errors, 
                 dashboards_errors = dashboards_errors,
                 total_schedules = count_schedule_errors, 
                 list_errors_schedules= schedule_errors,
                 total_pdt_errors = count_pdt_errors, 
                 list_pdt_errors = pdt_errors,
                 unlimited_queries = unlimited_queries, 
                 report_url = report_url,
                 is_clustered = is_instance_clustered, 
                 list_nodes = list_nodes,
                 total_connections = count_connections, 
                 list_errors_connections = connection_errors,
                 total_integrations = count_integrations, 
                 list_errors_integrations = integration_errors,
                 total_datagroups = count_datagroups, 
                 list_errors_datagroups = datagroup_errors
                 )
logger.info('Created email attachment')


# create the body of the email with summary data
content_email = email_body(looker_url = looker_url, 
                            looker_version = looker_version, 
                            total_users = all_users,
                            total_projects = count_all_projects, 
                            total_erring_content = count_content_errors,
                            total_schedules = count_all_schedules, 
                            total_pdt_errors = count_pdt_errors,
                            pdt_less_30 = pdt_build_times[0], 
                            pdt_30_60 = pdt_build_times[1], 
                            pdt_over_60 = pdt_build_times[2],
                            unlimited_queries = unlimited_queries,
                            total_connections = count_connections, 
                            total_integrations = count_integrations, 
                            total_datagroups = count_datagroups
                           )
logger.info('Created email body for report')

send_report_out(content=content_email)
logger.info('Sent email out with report')

logger.success('Themis process completed successfully.')