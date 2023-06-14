
#!/bin/sh
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#........................................................................
# Purpose: Deploy image on Cloud Run 
#........................................................................

SERVICE_NAME='TO_DO_DEVELOPER'
REGION='TO_DO_DEVELOPER'
PROJECT_ID='TO_DO_DEVELOPER'

GCLOUD_BIN=`which gcloud`

LOG_DATE=`date`
echo "###########################################################################################"
echo "${LOG_DATE} Deploying image to Cloud Run....."
"${GCLOUD_BIN}" run deploy ${SERVICE_NAME} --source . --platform managed --region ${REGION} --allow-unauthenticated

LOG_DATE=`date`
echo "###########################################################################################"
echo "${LOG_DATE} Execution finished! ..."