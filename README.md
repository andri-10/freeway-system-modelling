# Freeway System Modelling

A Python-based simulation framework for modeling freeway traffic systems using the Asymmetric Cell Transmission Model (ACTM). This project implements various traffic control strategies including open-loop control, linear controllers, PI controllers, and AI-enhanced controllers for ramp metering and traffic flow optimization.

## Features

- **Traffic Simulation**: Implements the ACTM for realistic freeway traffic modeling
- **Multiple Control Modes**:
  - Open-loop (no control)
  - Linear ramp metering controller
  - PI (Proportional-Integral) controller
  - AI-enhanced PI controller with demand prediction
- **Demand Prediction**: Machine learning model for predicting traffic demand patterns
- **Visualization**: Comprehensive plotting capabilities for density heatmaps, surface plots, queue analysis, and ramp flows
- **Performance Metrics**: Automated computation and comparison of traffic performance metrics
- **Scenario Management**: Flexible scenario building for different traffic conditions

## Project Structure

```
freeway-system-modelling/
├── pyproject.toml          # Project configuration and dependencies
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── src/                   # Source code
│   ├── main.py            # Main simulation script
│   ├── actm.py            # Asymmetric Cell Transmission Model implementation
│   ├── simulator.py       # Simulation engine
│   ├── scenario.py        # Scenario building utilities
│   ├── metrics.py         # Performance metrics calculation
│   ├── plotting.py        # Visualization functions
│   ├── ai/                # AI components
│   │   ├── __init__.py
│   │   ├── demand_predictor.py  # ML demand prediction model
│   │   └── train.py       # Training script for AI model
│   └── controllers/       # Traffic controllers
│       ├── linear_controller.py
│       └── pi_controller.py
└── results/               # Output directory
    └── metrics/           # Metrics and trained models
        └── comparison.csv # Performance comparison results
```

## Installation

### Prerequisites

- Python 3.14 or higher
- pip package manager

### Setup

1. Clone or download the project to your local machine

2. Navigate to the project directory:
   ```bash
   cd freeway-system-modelling
   ```

3. Install dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```

   Or using the pyproject.toml:
   ```bash
   pip install -e .
   ```

## Usage

### Training the AI Model (Required for AI mode)

Before running simulations with AI control, you need to train the demand predictor:

```bash
python src/ai/train.py
```

This will generate training data, train the model, and save it to `results/metrics/predictor.pkl`.

### Running Simulations

The main simulation script supports different control modes:

#### Single Mode Simulation

Run a simulation with a specific control mode:

```bash
# Open-loop (no control)
python src/main.py -m open

# Linear controller
python src/main.py -m linear

# PI controller
python src/main.py -m pi

# AI-enhanced PI controller (requires trained model)
python src/main.py -m ai
```

#### Compare All Modes

Run simulations for all control modes and generate a comparison:

```bash
python src/main.py -m all
```

This will:
- Run simulations for all modes (open, linear, pi, ai)
- Generate performance metrics for each mode
- Save comparison results to `results/metrics/comparison.csv`
- Display the comparison table

### Output Files

After running simulations, the following files are generated in the `results/` directory:

- `density_{mode}.png` - Traffic density heatmap
- `density_surface_{mode}.png` - 3D density surface plot
- `queues_{mode}.png` - Queue length plots for all ramps
- `flows_{mode}.png` - Ramp flow plots
- `metrics/comparison.csv` - Performance metrics comparison (when using `-m all`)

## Dependencies

- **numpy**: Numerical computing
- **matplotlib**: Plotting and visualization
- **pandas**: Data manipulation and analysis
- **scikit-learn**: Machine learning for demand prediction

## Configuration

The simulation parameters can be modified in `src/scenario.py`:

- Road network configuration
- Traffic demand patterns
- Controller parameters
- Simulation time steps

## Performance Metrics

The framework computes several key performance indicators:

- Total Travel Time (TTT)
- Total Travel Distance (TTD)
- Average Speed
- Queue lengths at ramps
- Flow rates

## Contributing

This is an academic/simulation project. For modifications:

1. Ensure all dependencies are installed
2. Test changes with different control modes
3. Verify that metrics are computed correctly
4. Update documentation as needed

## License

This project is for educational and research purposes. Please check with the original authors for usage permissions.
