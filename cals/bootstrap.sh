# Is the venv already created?
if [ ! -d "venv" ]; then
    # Create the venv
    python3 -m venv venv
fi

# Activate the venv
source venv/bin/activate

# Install dependencies
cd cals-sdk
pip install -e .
./setup_cals_sdk.sh

cd ../cals-server
pip install -e .
