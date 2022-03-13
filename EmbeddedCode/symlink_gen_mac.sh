find . -maxdepth 1 -mindepth 1 -type d \
		-not -path "./ExternalLibraries" \
		-not -path "./ControlLibraries" \
		-not -path "./Sensors" \
		-not -path "./Utility" \
		-exec ln -sfn $PWD/'{}' ~/Documents/Arduino/libraries/'{}' \;

cd ExternalLibraries
find . -maxdepth 1 -mindepth 1 -type d \
		-exec ln -sfn $PWD/'{}' ~/Documents/Arduino/libraries/'{}' \;

cd ../ControlLibraries
find . -maxdepth 1 -mindepth 1 -type d \
		-exec ln -sfn $PWD/'{}' ~/Documents/Arduino/libraries/'{}' \;
		
cd ../Sensors
find . -maxdepth 1 -mindepth 1 -type d \
		-exec ln -sfn $PWD/'{}' ~/Documents/Arduino/libraries/'{}' \;

cd ../Utility
find . -maxdepth 1 -mindepth 1 -type d \
		-exec ln -sfn $PWD/'{}' ~/Documents/Arduino/libraries/'{}' \;
