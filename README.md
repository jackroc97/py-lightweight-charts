# PyLightweightCharts

A python wrapper for [lightweight-charts](https://github.com/tradingview/lightweight-charts).

## How to Build & Install this Library

### Clone this repo from GitHub
```bash
# Clone the py-lightweight charts library
git clone https://github.com/jackroc97/py-lightweight-charts.git
cd py-lightweight-charts
```

### Clone the lightweight-charts library and build
```bash
# Clone and build lightweight-charts project (requires npm)
git clone https://github.com/tradingview/lightweight-charts.git
cd lightweight-charts
npm install
cd website
npm install

# Build the lightweight-charts project per their instructions
cd ../
npm run build:prod
```

### Build this library
```bash
# Copy the built lightweight-charts library to the `static` folder in py-lightweight-charts
cp dist/lightweight-charts.standalone.production.js ../src/py_lightweight_charts/static

# Build py-lightweight-charts
cd ../
python -m build .
```

### Install this library
```bash
python -m pip install dist/py_lightweight_charts-0.0.1-py3-none-any.whl
```