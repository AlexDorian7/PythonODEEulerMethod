echo "Please make sure you have python 3 installed under the command python3"

python3 -m venv ./venv
cd ./venv/bin
./pip3 install matplotlib==3.8.3
./pip3 install PyQt5==5.15.10
cd ../../

echo "Installed"
