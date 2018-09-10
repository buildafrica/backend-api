eval $(aws ecr get-login --region us-west-2 --no-include-email) 
docker push 496397425809.dkr.ecr.us-west-2.amazonaws.com/mpa:latest