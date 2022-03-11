sudo sysctl net.ipv4.conf.all.forwarding=1
sudo iptables -P FORWARD ACCEPT
sudo xhost +
sudo /etc/init.d/core-daemon start