docker build -t mpa --build-arg env=$DCMPA_ENVIRONMENT \
    --build-arg name=$POSTGRES_DB_NAME --build-arg user=$POSTGRES_DB_USER \
    --build-arg passwd=$POSTGRES_USER_PASSWORD -p 5432:5432 .