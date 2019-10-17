
# Plugin parameters
SERVICE_ACCOUNT_NAME=credentials-file

all: add-iam-policy publisher subscriber editor create-file

add-iam-policy:
	@echo "###Creating iam service-account for ${SERVICE_ACCOUNT_NAME}"
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

editor:
	@echo "### Adding editor's role file for project ${PROJECT_ID}"
	gcloud projects add-iam-policy-binding ${PROJECT_ID}\
    --member "serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"\
    --role "roles/editor"

create-file:
	@echo "### Creating credentials file for project ${PROJECT_ID}"
	gcloud iam service-accounts keys create ${SERVICE_ACCOUNT_NAME}.json\
    --iam-account ${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com