import jinja2
from weasyprint import HTML
from weasyprint import CSS


def email_body(looker_url, looker_version, total_users, total_projects, 
                total_erring_content, total_schedules,
               total_pdt_errors, pdt_less_30, pdt_30_60, pdt_over_60, 
               unlimited_queries, total_connections, total_integrations, 
               total_datagroups):
  '''Generates the summary body for the email'''
  body = '''
    Today's Report:<br><br>
    Looker instance: {}<br>
    Looker version: {}
    <br>
    <br>👤  <strong><font color="#4d5170" size="4">Users Summary</font></strong><br>
        {} users in the instance.
    <hr>
    <br>💻  <strong><font color="#4d5170" size="4">Projects LookML Validation</font></strong><br>
        {} projects in the instance.
    <hr>
    <br>📊  <strong><font color="#4d5170" size="4">Content Validation</font></strong><br>
        {} content with errors in the instance.
    <hr>
    <br>📩️  <strong><font color="#4d5170" size="4">Schedules</font></strong><br>
        {} schedules in the instance.
    <hr>
    <br>🚧  <strong><font color="#4d5170" size="4">PDTs</font></strong><br>
        {} PDTs failing in the instance.
        <br>Successful PDT builds are split into the following build times:
        <br>0-30 min: {} PDTs
        <br>30-60 min: {} PDTs
        <br>60+ min: {} PDTs
    <hr>
    <br>⏱  <strong><font color="#4d5170" size="4">Performance</font></strong><br>
        {}
    <hr>
    <br>🔑  <strong><font color="#4d5170" size="4">Connectivity</font></strong><br>
        {} connections in the instance.<br>
        {} integrations in the instance.<br>
        {} datagroups in the instance.<br>
    <br><br>
    <font color="grey" size="1">
        Find more information <a href="https://github.com/looker-open-source/Themis">go to the repo</a>
    <br>
        Something Wrong? <a href="https://github.com/looker-open-source/Themis">Tell us</a>
    </font>'''.format(looker_version,
                        looker_url,
                        total_users,
                        total_projects,
                        total_erring_content,
                        total_schedules,
                        total_pdt_errors,
                        pdt_less_30, pdt_30_60, pdt_over_60,
                        unlimited_queries,
                        total_connections,
                        total_integrations,
                        total_datagroups)
  return body


def email_attachment(looker_version, looker_url, total_users, user_details, total_projects,
                     total_erring_content, total_look_errors, look_errors, total_dash_errors, dashboards_errors,
                     total_schedules, list_errors_schedules, total_pdt_errors, list_pdt_errors,
                     unlimited_queries, report_url, is_clustered, list_nodes,
                     total_connections, list_errors_connections,
                     total_integrations, list_errors_integrations,
                     total_datagroups, list_errors_datagroups):
  '''Generates the detailed attachment for the email'''
  templateLoader = jinja2.FileSystemLoader(searchpath="./modules/rendering")
  template_env = jinja2.Environment(loader=templateLoader)
  TEMPLATE_FILE = "template_attachment.html"
  template = template_env.get_template(TEMPLATE_FILE)

  output_text = template.render(looker_version = looker_version,
                                looker_url = looker_url,
                                total_users = total_users,
                                user_details = user_details,
                                total_projects = total_projects,

                                total_erring_content = total_erring_content,
                                total_look_errors = total_look_errors,
                                look_errors = look_errors,
                                total_dash_errors = total_dash_errors,
                                dashboards_errors = dashboards_errors,

                                total_schedules = total_schedules,
                                list_errors_schedules = list_errors_schedules,
                                total_pdt_errors = total_pdt_errors, 
                                list_pdt_errors = list_pdt_errors,
                                
                                unlimited_queries = unlimited_queries, 
                                report_url = report_url, 
                                is_clustered = is_clustered, 
                                list_nodes = list_nodes,
                                  
                                total_connections = total_connections,
                                list_errors_connections = list_errors_connections,

                                total_integrations = total_integrations,
                                list_errors_integrations = list_errors_integrations,

                                total_datagroups = total_datagroups,
                                list_errors_datagroups = list_errors_datagroups
                                )
  html_file = open('./modules/rendering/rendered_version.html', 'w')
  html_file.write(output_text)
  html_file.close()
  HTML(filename='./modules/rendering/rendered_version.html').write_pdf('./modules/rendering/final_attachment.pdf', 
      stylesheets=[CSS(string='@page {{ font-family:arial, serif; font-size: 6; }}')])

  return 'Attachment created'
