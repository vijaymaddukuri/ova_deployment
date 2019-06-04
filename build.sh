#!/bin/sh
DIRECTORY="dist"
if [ -d "$DIRECTORY" ]; then
  # Control will enter here if $DIRECTORY exists.
  echo "Removing old artifacts"
  rm -rf dist/ build/

fi

python manage.py collectstatic

echo "Generating distribution archives"
python setup.py sdist bdist_wheel
