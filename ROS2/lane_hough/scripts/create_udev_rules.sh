#!/bin/bash
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}==== Create udev rules for SRC ====${NC}"
if [ -d /etc/udev/rules.d/src_udev.rules ]
then
	echo -e "${RED} delete exist file ${NC}"
	#rm -rf /etc/udev/rules.d/src_udev.rules
fi

sudo cp src_udev.rules /etc/udev/rules.d/src_udev.rules
echo " "
echo "reload udev rules"
sudo udevadm control --reload-rules && sudo udevadm trigger
echo "udev rules reload done"
echo "finish "