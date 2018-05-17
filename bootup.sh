# VARIABLES
ACCESS_TOKEN=$1
APPS=$2


# DO NOT TOUCH
IP=$(curl http://169.254.169.254/metadata/v1/interfaces/public/0/ipv4/address)
dvm server --kill
dvm login --access-token="$ACCESS_TOKEN" --endpoint="http://$IP"

for app in $APPS
do
   dvm enroll --app="$app"
done

dvm server --detached