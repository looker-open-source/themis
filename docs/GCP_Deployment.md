# Themis Deployment Guide for GCP Compute Engine

Thanks for using Themis, below is the 11 step list to getting it working!

1. Navigate to your GCP Console [[link]](https://console.cloud.google.com/compute/instances)

2. Once in the CGP Console, go to the page to create a Compute Engine instance
![](/docs/img/GCP/step1_open_cloud_console.png "Opening Cloud Console")


3. Select the suggested VM or modify parameters you need (You may want to increase to a e2-standard-2 type machine)
![](/docs/img/GCP/step2_create_vm.png "Creating the VM Instance")

4. Wait for the VM to spin up

5. Once the instance has been created and is running we will connect to it.
![](/docs/img/GCP/step3_connect_to_vm.png "Connecting to the VM")

6. In the **Connect** section of the page, click on the drop down and select the **Open Browser Window** option

7. Set up the VM
- `$ sudo apt-get update`
- `$ sudo apt-get install git` Install git
- `$ git --version`  Confirm git was installed and shows version
- `$ python3 --version`  Ensure Python 3 is installed
- `$ sudo apt install python3-pip`  Install pip for Python 3 if needed
- `$ pip3 --version`  Confirm pip3 was installed

8. Set up the Repo & dependencies
- `$ git clone https://github.com/looker-open-source/themis.git`  Clone the Themis repo
- `$ cd Themis`  Navigate into the directory
- `$ pip3 install -r requirements.txt`  Install the dependencies
- `$ sudo apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info` Install dependencies for the rendering package for the PDF report

9. Set up the script variables
- `$ vi looker.ini`  Create the Looker file for authentication
- Setting Up Env Var Create environment variables for SENDGRID_API_KEY and THEMIS_EMAIL_RECIPIENTS 

10. Run the application
- `$ python3 main.py`	Runs the application
Expected output from script:
```
> Checking instance: https://COMPANY.dev.looker.com
>>> Checked: USERS IN LOOKER in 0.8229 sec so far
>>> Checked: PROJECTS IN LOOKER in 1.0607 sec so far
>>> Checked: CONTENT IN LOOKER in 124.0097 sec so far
>>> Checked: SCHEDULES IN LOOKER in 128.0676 sec so far
>>> Checked: CONNECTIVITY IN LOOKER in 176.1308 sec so far
>>> Created email attachment 177.2215 sec so far
>>> Created email body 177.2216 sec so far
>>> Sent email out 177.6384 sec so far
>>> Completed process in 177.6385 seconds
```

11. You can use [Cloud Scheduler](https://cloud.google.com/scheduler/docs/quickstart#create_a_job) to set the application to run on a specific interval.




