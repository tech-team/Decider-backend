# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "ubuntu/trusty64"

  config.vm.synced_folder "./", "/home/vagrant/decider-backend/"

  config.vm.provision "shell",
    privileged: false,
    path: "provision/run.sh"

  config.vm.network :forwarded_port, host: 8888, guest: 8000

  config.vm.provider "virtualbox" do |v|
    v.memory = 1600
    v.cpus = 2
    v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    v.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
  end

end
