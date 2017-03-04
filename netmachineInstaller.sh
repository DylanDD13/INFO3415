python -m pip install ipaddr 
wget http://lcamtuf.coredump.cx/p0f3/releases/p0f-latest.tgz
tar xzf p0f-latest.tgz
cd p0f-3.09b
sudo apt-get install build-essential libpcap-dev
make
cd tools
make
cd..
cp p0f /usr/local/bin/
cp p0f.fp /etc/
cp tools/p0f-client /usr/local/bin/ 
python -m pip install p0f
