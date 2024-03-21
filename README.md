Install  python 3.X 
Install Homebrew 
Install cask "brew install cask"
Install chromedriver "brew install cask chromedriver"
Check the Chrome driver version chromedriver --version
Install Git 
Install Pycharm 
Clone the project
Open the cloned project in Pycharm
Open terminal
Update pip curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
Install virtual environment pip3 install virtualenv
Create virtual environment virtualenv -p python3 venv_name
Activate virtual environment source venv_name/bin/activate
Check that virtual environment has python 3.x version python --version
Optional : if you want to deactivate the virtual environment, run deactivate
Install requirements pip3 install -r requirements.txt (make sure that the virtual environment is activated)
Run tests using th following command "pytest tests/order_placement_tests.py"
