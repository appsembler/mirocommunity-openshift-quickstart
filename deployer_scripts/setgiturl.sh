OPENSHIFT_APP_NAME="$1"

SSH_URL=`rhc app show $OPENSHIFT_APP_NAME | grep ssh | cut -d" " -f5 `
# for test

echo $SSH_URL

git remote add rhc $SSH_URL

echo "git remote url \"rhc\" has been set to $SSH_URL"