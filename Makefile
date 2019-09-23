
# Plugin parameters
SERVICE_ACCOUNT_NAME=credentials-file

all: add-iam-policy publisher subscriber create-file

add-iam-policy:
	gcloud iam service-accounts create ${SERVICE_ACCOUNT_NAME}

publisher:
	@echo "### Adding publisher's role file for project ${PROJECT_ID}"
	gcloud projects add-iam-policy-binding ${PROJECT_ID}\
    --member "serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"\
    --role "roles/pubsub.publisher"

subscriber:
	@echo "### Adding subscriber's role file for project ${PROJECT_ID}"
	gcloud projects add-iam-policy-binding ${PROJECT_ID}\
    --member "serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"\
    --role "roles/pubsub.subscriber"

create-file:
	@echo "### Creating credentials file for project ${PROJECT_ID}"
	gcloud iam service-accounts keys create ${SERVICE_ACCOUNT_NAME}.json\
    --iam-account ${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com