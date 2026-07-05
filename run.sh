#!/usr/bin/env bash

# Terminal Colors for Professional Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color (reset formatting)
BOLD='\033[1m'

# 1. Verify the script is executed from the project root
if [ ! -f "pyproject.toml" ] || [ ! -d "backend" ]; then
    echo -e "${RED}${BOLD}Error:${NC} This script must be executed from the project root directory containing pyproject.toml and backend/."
    exit 1
fi

echo -e "${BLUE}${BOLD}>>> Starting Agentic SOC Backend Services <<<${NC}"

# 2. Verify the venv exists
if [ ! -d "venv" ] || [ ! -f "venv/bin/activate" ]; then
    echo -e "${RED}${BOLD}Error:${NC} Virtual environment 'venv' was not found in the project root."
    echo -e "Please initialize the environment: ${YELLOW}python3 -m venv venv${NC}"
    exit 1
fi

# 3. Activate the virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Check if Python is executable inside the environment
if ! command -v python &> /dev/null; then
    echo -e "${RED}${BOLD}Error:${NC} Python was not found in the active virtual environment path."
    exit 1
fi

# 4. Verify .env exists
if [ ! -f ".env" ]; then
    echo -e "${RED}${BOLD}Error:${NC} Configuration file .env was not found."
    if [ -f ".env.example" ]; then
        echo -e "${YELLOW}Tip:${NC} Create one by copying the example: ${GREEN}cp .env.example .env${NC}"
    fi
    exit 1
fi

# 5. Verify required Python packages are installed
echo -e "${BLUE}Verifying dependencies from requirements.txt...${NC}"
MISSING_DEPS=$(python -c "
import sys
from importlib.metadata import version, PackageNotFoundError

missing = []
try:
    with open('requirements.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # Parse package name, stripping bounds, and extras (e.g. uvicorn[standard]>=0.30.0 -> uvicorn)
            pkg_name = line.split('[')[0].split('>=')[0].split('==')[0].split('<')[0].strip()
            
            # Normalize pkg name for metadata checking
            norm_name = pkg_name.replace('_', '-').lower()
            try:
                version(norm_name)
            except PackageNotFoundError:
                try:
                    version(norm_name.replace('-', '_'))
                except PackageNotFoundError:
                    missing.append(pkg_name)
except FileNotFoundError:
    print('requirements.txt not found')
    sys.exit(2)

if missing:
    print(' '.join(missing))
    sys.exit(1)
")

STATUS=$?
if [ $STATUS -eq 1 ]; then
    echo -e "${RED}${BOLD}Error:${NC} The following required packages are missing or not installed in the venv: ${YELLOW}${MISSING_DEPS}${NC}"
    echo -e "Please run: ${GREEN}pip install -r requirements.txt${NC}"
    exit 1
elif [ $STATUS -eq 2 ]; then
    echo -e "${RED}${BOLD}Error:${NC} requirements.txt is missing from the project root."
    exit 1
fi

echo -e "${GREEN}Dependencies verified successfully.${NC}"

# 6. Print useful startup information
# Fetch properties dynamically from Settings to ensure they are loaded and verified
APP_NAME=$(python -c "from backend.core.config import settings; print(settings.APP_NAME)")
APP_ENV=$(python -c "from backend.core.config import settings; print(settings.APP_ENV)")
HOST=$(python -c "from backend.core.config import settings; print(settings.HOST)")
PORT=$(python -c "from backend.core.config import settings; print(settings.PORT)")

echo -e "\n${GREEN}${BOLD}--------------------------------------------------${NC}"
echo -e "${BOLD}Service:     ${NC}${APP_NAME}"
echo -e "${BOLD}Environment: ${NC}${APP_ENV}"
echo -e "${BOLD}Host:        ${NC}${HOST}"
echo -e "${BOLD}Port:        ${NC}${PORT}"
echo -e "${BOLD}Docs URL:    ${NC}http://${HOST}:${PORT}/docs"
echo -e "${GREEN}${BOLD}--------------------------------------------------${NC}\n"

# 7. Start the FastAPI backend using existing backend.run entry point
echo -e "${BLUE}Starting Uvicorn server...${NC}"
python -m backend.run
