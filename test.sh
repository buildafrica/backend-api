# Environment Variables needed for testing:
# - DCMPA_ENVIRONMENT
# - POSTGRES_DB_NAME
# - POSTGRES_DB_USER
# - POSTGRES_USER_PASSWORD
#
# Docker commands
# build: docker build -t subomi/mpa-staging --build-arg env=$DCMPA_ENVIRONMENT --build-arg name=$POSTGRES_DB_NAME --build-arg user=$POSTGRES_DB_USER  --build-arg passwd=$POSTGRES_USER_PASSWORD --add-host="postgreslocalhost:192.168.43.150" .
# run: docker run -it --add-host="postgreslocalhost:192.168.43.150" -p 8080:8080 subomi/mpa-staging


export DCMPA_ENVIRONMENT="local"
export POSTGRES_DB_NAME="Dcmpa"
export POSTGRES_DB_USER="postgres"
export POSTGRES_USER_PASSWORD="postgres"

# Execute test
python3 manage.py test