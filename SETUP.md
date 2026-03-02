# S2F-DT Installation Guide

If you're experiencing installation errors, follow this step-by-step guide.

## Windows Installation

### Option 1: Automated Script (Recommended)

Create a file named `setup.bat` in the project root and run it:

```batch
@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing dependencies...
pip install --no-cache-dir -r requirements.txt

echo Setup complete! Run: streamlit run app.py
pause
```

### Option 2: Manual Step-by-Step

1. **Create virtual environment:**
   ```powershell
   python -m venv venv
   ```

2. **Activate it:**
   ```powershell
   venv\Scripts\Activate.ps1
   ```

3. **Upgrade pip:**
   ```powershell
   python -m pip install --upgrade pip
   ```

4. **Install packages one by one** (if bulk install fails):
   ```powershell
   pip install streamlit
   pip install pandas
   pip install numpy
   pip install matplotlib
   pip install plotly
   pip install reportlab
   pip install pydantic
   pip install python-dotenv
   ```

5. **Verify installation:**
   ```powershell
   pip list
   ```

6. **Run the app:**
   ```powershell
   streamlit run app.py
   ```

---

## macOS Installation

```bash
# Create venv
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install --no-cache-dir -r requirements.txt

# Run
streamlit run app.py
```

---

## Common Issues & Solutions

### Issue 1: `No module named 'venv'`
**Solution:**
```powershell
# Windows - use full path
C:\Python311\python.exe -m venv venv

# macOS/Linux
python3.11 -m venv venv
```

### Issue 2: `pip is not recognized`
**Solution:** Use Python's pip module directly:
```powershell
python -m pip install -r requirements.txt
```

### Issue 3: Version conflicts
**Solution:** Use `--no-cache-dir` and relax version pins:
```powershell
pip install --no-cache-dir --upgrade-strategy only-if-needed -r requirements.txt
```

### Issue 4: reportlab compilation error
**Solution:** Install pre-built wheel:
```powershell
pip install --only-binary :all: reportlab
```

### Issue 5: Microsoft C++ build tools needed
**Solution:** Install Visual C++ Build Tools or use pre-compiled wheels:
```powershell
pip install --only-binary :all: numpy matplotlib
```

### Issue 6: SSL certificate error
**Solution:** Temporarily disable SSL verification (not recommended for production):
```powershell
pip install --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

---

## Docker Installation (Alternative)

Create `Dockerfile` in project root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

Build and run:
```bash
docker build -t s2f-dt .
docker run -p 8501:8501 s2f-dt
```

---

## Minimal Installation

If full installation fails, try this minimal version:

**`requirements_minimal.txt`:**
```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
```

Then install with:
```powershell
pip install -r requirements_minimal.txt
```

**Note:** PDF export and some visualizations won't work without reportlab and plotly, but core functionality will be available.

---

## Verify Installation

After installing, verify with:

```python
python -c "import streamlit; import pandas; import numpy; print('All core packages installed!')"
```

---

## Get Help

If issues persist:
1. Check Python version: `python --version` (should be 3.11+)
2. Check pip version: `pip --version`
3. Run: `pip list` to see what's actually installed
4. Check virtual environment is activated: `which python` (should show venv path)

---

## Support

For more help, see README.md in the project root.
