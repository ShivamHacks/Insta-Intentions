python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# rsync -av --exclude='.venv' . ec2-user@ec2-3-133-160-113.us-east-2.compute.amazonaws.com:/home/ec2-user/InstaIntentions/
