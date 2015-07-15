#!/bin/bash

export RABBITMQ_USER=decider_user
export RABBITMQ_PASS=decider_pass
export RABBITMQ_VHOST=decider_vhost


# Edit the following to change the name of the database user that will be created:
APP_DB_USER=decider_db_user
APP_DB_PASS=decider_db_pass

# Edit the following to change the name of the database that is created (defaults to the user name)
APP_DB_NAME=decider_db

PSQL_HOST=localhost
PSQL_PORT=5432

# Edit the following to change the version of PostgreSQL that is installed
export PG_VERSION=9.4

###########################################################
# Changes below this line are probably not necessary
###########################################################
print_db_usage () {
  echo "Your PostgreSQL database has been setup and can be accessed on your local machine on the forwarded port (default: 15432)"
  echo "  Host: $PSQL_HOST"
  echo "  Port: $PSQL_PORT"
  echo "  Database: $APP_DB_NAME"
  echo "  Username: $APP_DB_USER"
  echo "  Password: $APP_DB_PASS"
  echo ""
  echo "Admin access to postgres user via VM:"
  echo "  vagrant ssh"
  echo "  sudo su - postgres"
  echo ""
  echo "psql access to app database user via VM:"
  echo "  vagrant ssh"
  echo "  sudo su - postgres"
  echo "  PGUSER=$APP_DB_USER PGPASSWORD=$APP_DB_PASS psql -h $PSQL_HOST $APP_DB_NAME"
  echo ""
  echo "Env variable for application development:"
  echo "  DATABASE_URL=postgresql://$APP_DB_USER:$APP_DB_PASS@$PSQL_HOST:$PSQL_PORT/$APP_DB_NAME"
  echo ""
  echo "Local command to access the database via psql:"
  echo "  PGUSER=$APP_DB_USER PGPASSWORD=$APP_DB_PASS psql -h $PSQL_HOST -p $PSQL_PORT $APP_DB_NAME"
}

export DEBIAN_FRONTEND=noninteractive

export PROVISIONED_ON=/etc/vm_provision_on_timestamp
if [ -f "$PROVISIONED_ON" ]
then
  echo "VM was already provisioned at: $(cat $PROVISIONED_ON)"
  echo "To run system updates manually login via 'vagrant ssh' and run 'apt-get update && apt-get upgrade'"
  echo ""
  print_db_usage
  # exit
fi

PG_REPO_APT_SOURCE=/etc/apt/sources.list.d/pgdg.list
if [ ! -f "$PG_REPO_APT_SOURCE" ]
then
  # Add PG apt repo:
  sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

  # Add PGDG repo key:
  sudo apt-get install -y wget ca-certificates
  wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
fi

# Update package list and upgrade all packages
sudo apt-get update
sudo apt-get -y upgrade

# Needed for Pillow
sudo apt-get -y install "libjpeg-dev"

sudo apt-get -y install "postgresql-$PG_VERSION" \
                        "postgresql-contrib-$PG_VERSION" \
                         pgadmin3 \
                        "postgresql-server-dev-$PG_VERSION" \
                         libpq-dev

export PG_CONF="/etc/postgresql/$PG_VERSION/main/postgresql.conf"
export PG_HBA="/etc/postgresql/$PG_VERSION/main/pg_hba.conf"
export PG_DIR="/var/lib/postgresql/$PG_VERSION/main"

# Edit postgresql.conf to change listen address to '*':
sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" "$PG_CONF"

# Append to pg_hba.conf to add password auth:
sudo -E bash -c 'echo $PG_HBA && echo "host    all             all             all                     md5" >> "$PG_HBA"'

# Explicitly set default client_encoding
sudo -E bash -c 'echo $PG_CONF && echo "client_encoding = utf8" >> "$PG_CONF"'

# Restart so that all new config is loaded:
sudo service postgresql restart

sudo cat << EOF | sudo su - postgres -c psql
-- Create the database user:
CREATE USER $APP_DB_USER WITH PASSWORD '$APP_DB_PASS';

-- Create the database:
CREATE DATABASE $APP_DB_NAME WITH OWNER=$APP_DB_USER
                                  LC_COLLATE='en_US.utf8'
                                  LC_CTYPE='en_US.utf8'
                                  ENCODING='UTF8'
                                  TEMPLATE=template0;
EOF

# Tag the provision time:
sudo -E bash -c 'sudo date > "$PROVISIONED_ON"'

echo "Successfully created PostgreSQL dev virtual machine."
echo ""
print_db_usage

release=`lsb_release -c -s`

# PostgreSQL stuff


sudo apt-get install -y git \
						python2.7 \
						python-pip python2.7-dev

sudo pip install virtualenv


virtualenv ${HOME}/decider-backend/env/
${HOME}/decider-backend/env/bin/pip install -Ur ${HOME}/decider-backend/requirements.txt

echo ". /home/vagrant/decider-backend/env/bin/activate" >> ${HOME}/.bashrc

#if [ ${TRAVIS} == true ]; then
#	echo "TRAVIS"
    #sudo cp provision/tarantool.cfg /etc/tarantool/instances.enabled/tarantool.cfg
    #sudo cp provision/init.lua /usr/share/tarantool/lua/init.lua
#else
#	echo "ORDINAL"
    #sudo cp ${HOME}/tech-testing-ha1/provision/tarantool.cfg /etc/tarantool/instances.enabled/tarantool.cfg
    #sudo cp ${HOME}/tech-testing-ha1/provision/init.lua /usr/share/tarantool/lua/init.lua
#fi

sudo /etc/init.d/postgresql restart


# celery stuff

sudo apt-get -f install

sudo rabbitmqctl add_user $RABBITMQ_USER $RABBITMQ_PASS
sudo rabbitmqctl add_vhost $RABBITMQ_VHOST
sudo rabbitmqctl set_permissions -p $RABBITMQ_VHOST $RABBITMQ_USER ".*" ".*" ".*"

source ${HOME}/decider-backend/env/bin/activate

export CELERY_APP=push_service
export CELERY_MODULE=tasks

# tbd
celery -D -B -A $CELERY_APP.$CELERY_MODULE worker