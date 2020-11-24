import datetime

class Projects:
    'PROJECTS IN LOOKER'

    lookmlErrorCount = 0

    def __init__(self, looker_client):
        self.looker_client = looker_client

    def count_all_projects(self):
        '''Returns the number of projects'''
        return len(self.looker_client.all_projects(fields='id'))

    def all_projects(self):
        '''Returns the list of projects'''
        my_projects = self.looker_client.all_projects(fields='id,name')
        project_ids = []
        for i in enumerate(my_projects):
            project_ids.append(my_projects[i].id)
        return project_ids

    def validate_lookml(self, project_id):
        '''Returns LookML validation errors'''
        validation = self.looker_client.validate_project(project_id)
        if validation.errors:
            for i in enumerate(validation.errors):
                Projects.lookmlErrorCount += 1
                severity = validation.errors[i].severity
                message = validation.errors[i].message
            return severity, message

    @staticmethod
    def count_lookml_errors():
        '''Returns the number of validation issues'''
        return Projects.lookmlErrorCount

    def run_git_test(self, project_id):
        '''Runs the git tests and returns the test failures'''
        # need to change session to 'dev'
        self.looker_client.update_session({"workspace_id":"dev"})
        git_tests = []

        # exclude models from marketplace
        if "marketplace_" not in str(project_id):
            all_git_tests = self.looker_client.all_git_connection_tests(project_id)
            for test_id in all_git_tests:
                one_test = self.looker_client.run_git_connection_test(project_id, test_id.id)
                if one_test.status != "pass":
                    git_tests.append("Test ID: {} failed on Project: {}".format(test_id.id, project_id))
        else:
            pass
        # change session back to 'production'
        self.looker_client.update_session({"workspace_id": "production"})
        return git_tests

    def get_stale_branches(self, project_id):
        '''Returns the base URL for the Looker instance'''
        # https://help.github.com/en/github/administering-a-repository/viewing-branches-in-your-repository
        all_branches = self.looker_client.all_git_branches(project_id)
        stale_branches = []
        for branch in all_branches:
            if not branch.is_production and not branch.personal:
                last_commit = datetime.datetime.fromtimestamp(branch.commit_at)
                # Date difference (today - last commit) is over 90 days?
                if abs((datetime.datetime.utcnow() - last_commit).days) > 90:
                    stale_branches.append([project_id, branch.name])
        if stale_branches:
            return stale_branches

    def get_lookml_test(self, project_id):
        '''Finds the LookML tests'''
        return self.looker_client.all_lookml_tests(project_id) != '[]'

    def run_lookml_test(self, project_id):
        '''Runs the LookML tests'''
        results = self.looker_client.run_lookml_test(project_id)
        if not results:
            pass
            # return "No test set up on Project: {}".format(project_id)
        else:
            return results
