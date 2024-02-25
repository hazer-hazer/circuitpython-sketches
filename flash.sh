#! sh

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Pass filename and drive letter, please"
else
    sudo mount -t drvfs $2: /mnt/r
    sudo cp -r ./lib/* /mnt/r/lib/
    sudo cp -r $1 /mnt/r/code.py
fi
