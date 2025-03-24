#!/bin/bash
#check if correct number of arguments are provided
if [ $# -ne 3 ]; then
    echo "Usage: $0 fileNamePrefix serverName port"
    exit 1
fi

# Define your variables from command line arguments
fileNamePrefix=$1
serverName=$2
port=$3

# Get the certificate
echo | openssl s_client -servername $serverName -connect $serverName:$port 2>/dev/null | openssl x509 > temp.crt

# Extract the expiration date
expirationDate=$(openssl x509 -noout -dates -in temp.crt | grep notAfter | cut -d= -f2)

# Extract the year, month and day
expirationYear=$(date -d "$expirationDate" +%Y)
expirationMonth=$(date -d "$expirationDate" +%m)
expirationDay=$(date -d "$expirationDate" +%d)

# Generate the file name
fileName="${fileNamePrefix}_${expirationYear}_${expirationMonth}_${expirationDay}.crt"

# Rename the certificate file
mv temp.crt $fileName

# Echo the filename to stdout
echo $fileName