# Getting Started

## Prerequisites
- Python 3.8 or higher
- pip
- virtualenv

## Setup
1. Clone the repository
```bash
git clone https://github.com/DallasFormulaRacing/WebDashboard
```

2. Navigate to the root directory of the repository
```bash
cd WebDashboard
```

3. Create a virtual environment
```bash
python -m venv venv
```

4. Activate the virtual environment (Windows)
```bash
.\venv\Scripts\activate
```

5. Install the required packages
```bash
pip install -r requirements.txt
```

2. Navigate to the dashboard directory
```bash
cd dashboard
```

6. Run the dashboard
```bash
python app.py
```


## Dashboard File Structure

```
+-- Assets/
      |      +-- css
      |      +-- images
      |      +-- scripts

+-- Components/
      |      +-- footer
      |      +-- navbar
      |      +-- etc.
+-- Pages/
      |      +-- 404.py
      |      +-- aero.py
      |      +-- steeringsuspension.py
      |      +-- powertrain/
                      |      +-- visualizations/
                                    |     +-- rpm_over_time.py
                      |      +-- layout.py
+-- Utils/
      |      +-- common functions
+-- app.py
```
