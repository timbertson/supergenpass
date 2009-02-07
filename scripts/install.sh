# this is just a prototype; it doesn't *work* yet...
PREFIX='/opt/local'
pth="$PREFIX/etc/bash_completion.d"
mkdir -p "$pth"
rm "$pth/supergenpass"
ln -s `pwd`/complete.sh "$pth/supergenpass"

