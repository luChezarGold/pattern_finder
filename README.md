# Pattern Finder (MetaTrader5 Exported Data)

## Description  
This script is designed to analyze time-series data exported from MetaTrader5 or other sources in CSV format.  
It identifies recurring patterns in selected columns, calculates their frequency, and predicts potential outcomes  
based on historical trends.

## Features  
- **Data Loading**: Reads CSV files and extracts column values for analysis.  
- **Pattern Normalization**: Ensures consistent comparison by normalizing pattern values.  
- **Similarity Analysis**: Matches patterns within a configurable tolerance threshold.  
- **Outcome Prediction**: Analyzes historical trends to predict the next move (up or down).  
- **JSON Output**: Saves discovered patterns and their statistics in organized JSON files.

## File Structure  
```plaintext
.
├── pattern_analysis.py      # Main script for pattern discovery
├── prepared_delimiters_4.csv # Input CSV file (example)
├── patterns/                # Output directory for JSON results
│   ├── CLOSE_patterns_found.json
│   ├── VOLUME_patterns_found.json
│   └── ...

```
## Prerequisites  
- Python 3.6+  
- Libraries: `pandas`, `numpy`, `tqdm`, `json`  

## Usage  
- **Input File**: Place your MetaTrader5-exported CSV file in the script's directory.  
- **Excluded Columns**: Update the `exclude_columns` list to ignore unnecessary columns.  
- **Run the Script**:  
  ```bash
  python pattern_analysis.py
