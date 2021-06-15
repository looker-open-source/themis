
class Users:
    
    def __repr__(self):
        return 'USERS IN LOOKER'

    def __init__(self, looker_client):
        self.looker_client = looker_client

    def validate_api_creds(self):
        '''Ensures the API credentials tie to an Admin user'''
        # test admin credentials to access i_looker and see all instances elements
        api_user = self.looker_client.me()
        all_roles = []
        for role_id in api_user.role_ids:
            role = self.looker_client.role(role_id)
            all_roles.append(role.name.lower() == "admin")
        return True in all_roles

    def count_all_users(self):
        '''Returns number of users in the Looker instance'''
        return len(self.looker_client.all_users(fields='id'))

    def get_users_issue(self):
        '''Returns locked out users for the Looker instance'''
        all_users = self.looker_client.all_users(fields='id, is_disabled')
        disabled_users = []

        for i in all_users:
            if i.is_disabled:
                disabled_users.append(i)
        user_results = []
        user_results.append("Disabled Looker users: {}".format(len(disabled_users)))
        locked_out = self.looker_client.all_user_login_lockouts()
        user_results.append("Locked Out Looker users: {}".format(len(locked_out)))
        return user_results

    def get_inactive_users(self):
        '''Returns users without login data for past 90 days'''
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