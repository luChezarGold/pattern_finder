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
  ```

## Key Customization Points

### In pattern_analysis.py:

1. File Input Settings (Main Section):
```python
# CUSTOMIZE: Change input file name and delimiter
file_path = "prepared_delimiters_4.csv"  # Your input file
exclude_columns = ["DATE", "TIME", "OPEN", "HIGH", "LOW"]  # Columns to ignore
```

2. Pattern Detection Parameters (find_patterns function):
```python
# CUSTOMIZE: Adjust pattern detection sensitivity
min_length = 3      # Minimum pattern length
max_length = 12     # Maximum pattern length
tolerance = 0.2     # Pattern matching tolerance (0.0 to 1.0)
```

3. Output Settings (get_most_frequent_patterns function):
```python
# CUSTOMIZE: Change number of patterns to save
top_n = 5000  # Number of most frequent patterns to keep
```

4. Pattern Normalization (normalize_pattern function):
```python
# CUSTOMIZE: Modify normalization logic if needed
def normalize_pattern(pattern):
    min_val = min(pattern)
    max_val = max(pattern)
    return [(x - min_val) / (max_val - min_val) if max_val > min_val else 0 for x in pattern]
```

### Important Functions and Their Purposes:

1. `load_data()`:
   - WHAT: Loads CSV data and extracts specified columns
   - WHERE: Beginning of data processing pipeline
   - CUSTOMIZE: Column selection and delimiter

2. `normalize_pattern()`:
   - WHAT: Scales pattern values between 0 and 1
   - WHERE: Before pattern comparison
   - CUSTOMIZE: Normalization algorithm

3. `calculate_similarity()`:
   - WHAT: Compares two patterns for similarity
   - WHERE: During pattern matching
   - CUSTOMIZE: Similarity threshold and comparison method

4. `find_patterns()`:
   - WHAT: Main pattern discovery logic
   - WHERE: Core analysis function
   - CUSTOMIZE: Pattern length and tolerance parameters

5. `get_most_frequent_patterns()`:
   - WHAT: Selects top recurring patterns
   - WHERE: After pattern discovery
   - CUSTOMIZE: Number of patterns to save

## Configuration Parameters
- `min_length`: Minimum length of patterns to search for (default: 3)  
- `max_length`: Maximum length of patterns to search for (default: 12)  
- `tolerance`: Similarity threshold for pattern matching (default: 0.2)  
- `top_n`: Number of most frequent patterns to save (default: 5000)

## Input Data Format
The script expects a CSV file with the following characteristics:  
- Delimiter: "|" (pipe character)  
- Required columns: "DATE", "TIME", "OPEN", "HIGH", "LOW", "CLOSE"  
- Additional columns will be analyzed unless specified in `exclude_columns`

## Output Format
The script generates JSON files for each analyzed column with the following structure:  
```json
{
  "Pattern_12345": {
    "pattern": [0.0, 0.5, 1.0, 0.8],
    "count": 42,
    "next_move": 1
  }
}
```
- `pattern`: Normalized values of the pattern  
- `count`: Number of occurrences in the dataset  
- `next_move`: Predicted direction (1 for up, 0 for down)

## Performance Considerations
- Large datasets may require significant processing time  
- Memory usage scales with pattern length and dataset size  
- Progress bars indicate completion status for each processing stage

## Error Handling
The script includes basic error handling for:  
- Missing input files  
- Invalid column names  
- Insufficient data points  
- File system operations

## Contributing
Feel free to submit issues and enhancement requests!

## License
[MIT License](LICENSE)

## Acknowledgments
- Built for MetaTrader5 data analysis  
- Inspired by technical analysis pattern recognition techniques
