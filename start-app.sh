#!/usr/bin/env bash
echo "Starting App"

export token="NjdiZWYxZWNmYmExOTUwNDhjYTllYzU2Okw1Nks5N3gxU2QrY0xUTlI2NU5tWFhyV1ZLaG9FeW1FOVczUHZZSTVnYVk9"
export endpoint="https://app.datarobot.com/api/v2"
export app_base_url_path="https://app.datarobot.com/custom_applications/67beda95d21cac1b8613e24a/"

# If you have configured runtime params via DataRobots application source, the following 2 values should be set automatically.
# Otherwise you will need to set DEPLOYMENT_ID (required) and CUSTOM_METRIC_ID (optional) manually
if [ -n "$MLOPS_RUNTIME_PARAM_DEPLOYMENT_ID" ]; then
  export deployment_id="67bed90f403262b54d29c4f8"
else
  export deployment_id="67bed90f403262b54d29c4f8"
fi
if [ -n "$MLOPS_RUNTIME_PARAM_CUSTOM_METRIC_ID" ]; then
  export custom_metric_id="67bef2f8182bcf1864b87f69"
else
  export custom_metric_id="67bef2f8182bcf1864b87f69"
fi

streamlit-sal compile
streamlit run --server.port=8080 qa_chat_bot.py