# Themis Deployment Guide for Heroku

Thanks for using Themis, below is the 11 step list to getting it working!

1. [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/llooker/themis/tree/master)

2. On the configuation page enter a unique name for the application and input the variables listed on the page. (If you are not using a `looker.ini` file for Looker authentication, you will need to input values for the 3 LOOKERSDK config vars). Below is an example of the process using fake values

![](/docs/img/Heroku/step1_enter_vars.png "Creating the VM Instance")

3. Confirm all the deployment steps were succesful. Click on **Manage App**
![](/docs/img/Heroku/step2_app_deployment.png "Creating the VM Instance")

#### The application is now built successfulyl and deployed on the Heroku server!

------------
   
You can now add a Scheduler add-on to control the application run. 
Below are the steps covering one of the available scheduling add-on for heroku.

4. Click **Configure Add-ons ➡**

5. Search for "heroku scheduler" and select it
6. Select the "Standard - Free Plan" and click **Provision**
![](/docs/img/Heroku/step3+provision_scheduler.png "Heroku Scheduler Provisioning modal")

7. You should see a notification the page: `The add-on scheduler has been installed. Check out the documentation in its Dev Center article to get started.` Below will be the list of add-ons. Click on the **Heroku Scheduler**
8. Once on the page for the scheduler, click **Create Job**
![](/docs/img/Heroku/step4_Heroku_Scheduler.png "Define your Schedule Job")

⚠️ _Select a time where your instance is not busy so the Themis processes are not impacting your Looker users_

### Congratulation, you have now deployed and scheduled Themis to run.

-------------




