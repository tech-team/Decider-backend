#!/usr/bin/env bash

release=`lsb_release -c -s`

# PostgreSQL stuff
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
sudo apt-get install -y wget ca-certificates
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

sudo apt-get update
sudo apt-get -y dist-upgrade
sudo apt-get install -y postgresql-9.4 pgadmin3

sudo apt-get install -y git \
						python2.7 \
						python-pip python2.7-dev

sudo pip install virtualenv

virtualenv ${HOME}/decider-backend/env/
${HOME}/decider-backend/env/bin/pip install -Ur ${HOME}/decider-backend/requirements.txt

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
