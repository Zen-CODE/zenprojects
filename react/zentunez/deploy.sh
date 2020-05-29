#! /bin/bash
echo "Running the NPM build...."
npm run build
echo "Copying static files to static..."
rsync -avz "build/static" "../../../zenplayer/zenplayer/webserver"
rm -rf build/static
echo "Copying react application files..."
rsync -avz build/*.* "../../../zenplayer/zenplayer/webserver/static"
echo "Removing build..."
rm -rf build/
echo "All done!"