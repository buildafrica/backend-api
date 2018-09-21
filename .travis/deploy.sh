
set -ev

pip3 install awscli --upgrade
eval $(aws ecr get-login --region us-west-2 --no-include-email) 
docker build -t mpa --build-arg env=$DCMPA_ENVIRONMENT --build-arg name=$POSTGRES_DB_NAME --build-arg user=$POSTGRES_DB_USER  --build-arg passwd=$POSTGRES_USER_PASSWORD .
docker tag mpa:latest 496397425809.dkr.ecr.us-west-2.amazonaws.com/mpa:latest
docker push 496397425809.dkr.ecr.us-west-2.amazonaws.com/mpa:latest