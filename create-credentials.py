import os
import sys

# Plugin parameters
SERVICE_ACCOUNT_NAME="logzio-credentials-file"
PROJECT_ID = sys.argv[1]

# Plugin 'gcloud' commands
ADD_IAM_SERVICE_ACCOUNT_CMD = "gcloud iam service-accounts create %s" % SERVICE_ACCOUNT_NAME
REMOVE_IAM_SERVICE_ACCOUNT_CMD = "gcloud iam service-accounts delete %s@%s.iam.gserviceaccount.com" % (SERVICE_ACCOUNT_NAME, PROJECT_ID)
ADD_ROLE_CMD = "gcloud projects add-iam-policy-binding %s \
        --member serviceAccount:%s@%s.iam.gserviceaccount.com \
        --role roles/pubsub.editor" % (PROJECT_ID, SERVICE_ACCOUNT_NAME, PROJECT_ID)
DELETE_ROLE_CMD = "gcloud projects remove-iam-policy-binding %s \
        --member serviceAccount:%s@%s.iam.gserviceaccount.com \
        --role roles/pubsub.editor" % (PROJECT_ID, SERVICE_ACCOUNT_NAME, PROJECT_ID)
CREATE_KEY_CMD = "gcloud iam service-accounts keys create %s-credentials.json\
         --iam-account %s@%s.iam.gserviceaccount.com" % (PROJECT_ID, SERVICE_ACCOUNT_NAME, PROJECT_ID)


def build_file():
    os.system("gcloud init")
    build_iam_service()

def build_iam_service():
    print("###Creating iam service-account for %s" % SERVICE_ACCOUNT_NAME)
    if os.system(ADD_IAM_SERVICE_ACCOUNT_CMD) == 0:
        print("\n### The iam service-account for %s was succesfully created." % SERVICE_ACCOUNT_NAME)
        add_editor_role()
    else:
        # Service account under that name already exists.
        print("\n>>> The iam service-account for %s was not created, a service account under that name already exists.\n>>> Please press 'Y' to reslove the conflict.\n***Note: Before you delete please make sure you are set up to the correct project id.\n" % SERVICE_ACCOUNT_NAME)
        if os.system(REMOVE_IAM_SERVICE_ACCOUNT_CMD) != 0:
            # Could not remove iam service account, not connected to the correct project.
            print("\n>>> Could not reslove the conflict.")
            handle_permission_denied()
        else:
            os.system(DELETE_ROLE_CMD)
            print("\n>>> The conflict was resloved, please rerun 'python create-credenatials.py %s'" % PROJECT_ID)


def add_editor_role():
    print("### Adding editor's role file for project %s" % PROJECT_ID)
    if os.system(ADD_ROLE_CMD) == 0:
        print("\n### Editor's role was succesfully added.")
        create_key()
    else:
        # Could not delete role, not connected to the correct project
        os.system(DELETE_ROLE_CMD)
        os.system(REMOVE_IAM_SERVICE_ACCOUNT_CMD)
        handle_permission_denied()

def create_key():
    print("### Creating credentials file for project %s" % PROJECT_ID)
    if os.system(CREATE_KEY_CMD) == 0:
        print("\n### '%s-credentials.json' file was succesfully created!" % PROJECT_ID)
    else:
        print("\n>>> There was an error with creating the credentials file, please rerun 'python create-credenatials.py %s'" % PROJECT_ID)


def handle_permission_denied():
    while True:
        input_val = raw_input("\n>>> Please make sure you are logged in with the project id you gave when running this script.\n>>> Do you want to continue to login (or exit)? (Y/n):\n")
        # print(input_val)
        if input_val == 'Y' or input_val == 'y':
            print("\n>>> Inializing gcloud...")
            build_file()
            exit()
        if input_val == 'N' or input_val == 'n':
            print("\n>>> Exiting...")
            exit()

build_file()
