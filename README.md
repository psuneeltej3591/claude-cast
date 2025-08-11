# 🏀 Dream11 Basketball Pro - First Rank Strategy Guide

A comprehensive Streamlit application designed to help Dream11 basketball players achieve first rank by analyzing player statistics, team performance, and creating optimal team combinations.

## ✨ Features

### 🎯 Core Functionality
- **Player Performance Analysis**: Comprehensive statistics for top NBA players
- **Fantasy Points Calculation**: Dream11 scoring system implementation
- **Team Builder**: Automatic and manual team creation tools
- **Position Strategy**: Balanced team composition recommendations
- **Advanced Analytics**: Interactive charts and data visualization

### 📊 Key Metrics
- **Fantasy Points**: Primary scoring metric based on Dream11 rules
- **Value Score**: Efficiency and consistency combined metric
- **Consistency**: Player reliability factor
- **Position Balance**: Proper team composition analysis

### 🏆 Strategy Guide
- **Key Metrics Focus**: What to prioritize for first rank
- **Position Strategy**: Optimal player distribution
- **Pro Tips**: Expert advice for success
- **Recent Form Analysis**: Performance trends and patterns

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Method 1: Quick Start (Recommended)

#### For Linux/Mac:
```bash
# Make the script executable and run
chmod +x run_app.sh
./run_app.sh
```

#### For Windows:
```bash
# Double-click the batch file or run in command prompt
run_app.bat
```

### Method 2: Manual Setup

#### Step 1: Clone or Download
```bash
# If using git
git clone <repository-url>
cd dream11-basketball-pro

# Or download and extract the files manually
```

#### Step 2: Install Dependencies

**Option A: Direct Installation (if allowed)**
```bash
pip install -r requirements.txt
```

**Option B: Virtual Environment (Recommended)**
```bash
# Create virtual environment
python3 -m venv dream11_env

# Activate virtual environment
# On Linux/Mac:
source dream11_env/bin/activate
# On Windows:
dream11_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Option C: Using pipx (if available)**
```bash
pipx install streamlit
pip install pandas numpy plotly requests beautifulsoup4 lxml openpyxl
```

**Option D: System Package Manager (Ubuntu/Debian)**
```bash
sudo apt update
sudo apt install python3-streamlit python3-pandas python3-numpy python3-plotly
```

#### Step 3: Run the Application
```bash
streamlit run dream11_basketball_pro.py
```

The app will open in your default web browser at `http://localhost:8501`

## 🔧 Troubleshooting

### Common Issues

**1. "externally-managed-environment" Error**
- Use virtual environment method (Option B above)
- Or use system package manager (Option D above)

**2. "Module not found" Errors**
- Ensure all dependencies are installed
- Check if virtual environment is activated
- Verify Python version (3.8+)

**3. Permission Denied (Linux/Mac)**
```bash
chmod +x run_app.sh
```

**4. Port Already in Use**
```bash
# Kill existing Streamlit processes
pkill -f streamlit
# Or use different port
streamlit run dream11_basketball_pro.py --server.port 8502
```

### Environment-Specific Solutions

**Ubuntu/Debian:**
```bash
sudo apt install python3-venv python3-pip
python3 -m venv dream11_env
source dream11_env/bin/activate
pip install -r requirements.txt
```

**macOS:**
```bash
# Using Homebrew
brew install python3
python3 -m venv dream11_env
source dream11_env/bin/activate
pip install -r requirements.txt
```

**Windows:**
```bash
# Ensure Python is in PATH
python -m venv dream11_env
dream11_env\Scripts\activate
pip install -r requirements.txt
```

## 🎮 How to Use

### 1. **Player Analysis**
- View top performers by fantasy points
- Filter players by position and minimum fantasy points
- Analyze individual player statistics

### 2. **Team Building**
- **Auto-Generate**: Click "Generate Optimal Team" for AI-powered suggestions
- **Manual Selection**: Choose up to 8 players manually
- **Team Composition**: View position distribution and total fantasy points

### 3. **Strategy Planning**
- Study the First Rank Strategy Guide
- Focus on key metrics and position balance
- Follow pro tips for better decision making

### 4. **Advanced Analytics**
- Interactive scatter plots and charts
- Position-wise performance analysis
- Recent form trends and patterns

## 📈 Dream11 Scoring System

The app calculates fantasy points using the following formula:
```
Fantasy Points = 
  (Points × 1.0) +
  (Rebounds × 1.5) +
  (Assists × 2.0) +
  (Steals × 3.0) +
  (Blocks × 3.0) +
  (Field Goal % - 40) × 0.1 +
  (3-Point % - 30) × 0.1 +
  (Free Throw % - 70) × 0.1
```

## 🎯 First Rank Strategy

### **Key Principles**
1. **Balance**: Maintain 2-3 players per position
2. **Consistency**: Choose reliable performers
3. **Value**: Focus on high-value players
4. **Form**: Consider recent performance trends

### **Position Strategy**
- **PG/SG**: High assist and scoring potential
- **SF**: Balanced scoring and all-around play
- **PF/C**: Rebound and block specialists
- **Team Balance**: Avoid overloading any single position

### **Pro Tips**
- Monitor injury reports before game day
- Check recent form trends (last 5 games)
- Consider home/away game factors
- Analyze head-to-head matchups
- Don't chase last game's performance

## 🔧 Customization

### Adding New Players
Edit the `load_sample_data()` function in `dream11_basketball_pro.py` to add more players or modify existing data.

### Modifying Scoring System
Adjust the fantasy points calculation in the same function to match your league's specific rules.

### Data Sources
In a production environment, replace the sample data with:
- Real-time API calls to basketball statistics services
- Database connections
- Web scraping from official sources

## 📱 App Structure

```
dream11_basketball_pro.py    # Main application file
requirements.txt             # Python dependencies
run_app.sh                  # Linux/Mac launcher script
run_app.bat                 # Windows launcher script
README.md                   # This documentation file
```

## 🎨 UI Features

- **Responsive Design**: Works on desktop and mobile devices
- **Interactive Charts**: Plotly-powered visualizations
- **Custom CSS**: Modern, professional appearance
- **Sidebar Navigation**: Easy access to all features
- **Color-Coded Positions**: Visual position identification

## ⚠️ Important Notes

- **Demo Data**: This app uses sample data for demonstration
- **Real-Time Updates**: For live competitions, integrate with real-time data sources
- **Verification**: Always verify player availability and injury status
- **Responsibility**: Use this tool as a guide, not guaranteed success

## 🚀 Future Enhancements

- **Real-Time Data**: Live player statistics and injury updates
- **Historical Analysis**: Player performance over time
- **League Integration**: Direct Dream11 API integration
- **Mobile App**: Native mobile application
- **Social Features**: Team sharing and community rankings

## 🤝 Contributing

Feel free to contribute improvements, bug fixes, or new features by:
1. Forking the repository
2. Creating a feature branch
3. Making your changes
4. Submitting a pull request

## 📄 License

This project is for educational and personal use. Please respect Dream11's terms of service and use responsibly.

## 🆘 Support

For issues or questions:
- Check the documentation above
- Review the code comments
- Create an issue in the repository

---

**🏀 Good luck with your Dream11 basketball journey! May you achieve that first rank! 🏆**
