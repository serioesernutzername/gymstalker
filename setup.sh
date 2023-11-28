
if git clone https://github.com/serioesernutzername/gymstalker.git ; then
  cd ./gymstalker/
  rm setup.sh
  if pip install -r ./requirements.txt; then
    clear
    echo "Webscraper successfully installed! Please wait..."
    sleep 5
    if python ./webscraper/main.py; then
      echo "The application is running."
    else
      echo "Failed to run the application."
    fi
  else
    echo "Failed to install dependencies."
  fi
else
  echo "Failed to download the repository."
fi
