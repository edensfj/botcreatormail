geoip="./geoip"
geoip6="./geoip6"

TEMP_PATH="/tmp"

rm -rf torrc*
for (( i = 0; i < 12; i++ )); do
# rand="$RANDOM"
rand="905$i"
mkdir -p "$TEMP_PATH/torrc_$rand"
DEST_FILE="$TEMP_PATH/torrc_$rand/geoip_$i"
DEST_FILE6="$TEMP_PATH/torrc_$rand/geoip6_$i"
cp $geoip $DEST_FILE
cp $geoip6 $DEST_FILE6
read -r -d '' CONFIG << EOM
SocksPort 0.0.0.0:$rand
CircuitBuildTimeout 3
LearnCircuitBuildTimeout 0
MaxCircuitDirtiness 3
DataDirectory $TEMP_PATH/torrc_$rand
GeoIPFile $TEMP_PATH/torrc_$rand/geoip_$i
GeoIPv6File $TEMP_PATH/torrc_$rand/geoip6_$i
EOM
echo "$CONFIG" > "$TEMP_PATH/torrc$rand"
xterm -e "tor -f $TEMP_PATH/torrc$rand"&
done
echo "CORRIENDO TERMINALES";
