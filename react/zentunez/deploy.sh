#! /bin/bash
echo "Running the NPM build...."
npm run build
echo "Copying static files to static..."
rsync -avz "build/static" "../../python/django/tunez/"
echo "Copying react application files..."
rsync -avz build/*.* "../../python/django/tunez/react/"
echo "Removing build..."
rm -rf build/
echo "All done!"