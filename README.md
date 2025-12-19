# 🏭 Industrial Optimizer: Multi-Block System

An intelligent industrial optimization system for complex inventory management and cutting line calculations using Artificial Intelligence.

## 📋 Description

**Industrial Optimizer** is a web application built with Streamlit that uses AI agents (GPT-4o-mini) to solve "3D Bin Packing" optimization problems. The system analyzes material block inventories and calculates optimal cutting points to fulfill customer orders while minimizing waste.

### Key Features

- 🤖 **Multi-Agent System**: Two specialized agents collaborate for technical analysis and executive reports
- 📐 **Geometric Analysis**: Precise calculations using "Big Rocks First" algorithms for cut optimization
- 📊 **Graphical Visualization**: Visual representation of cutting plans per block
- 💾 **Persistence**: Prediction history stored in SQLite
- 🎨 **Multi-Color Support**: Management of multiple production lines (Blue, Red, Green, etc.)

## 🏗️ Architecture

```
industrial/
├── cuts/
│   ├── app.py          # Main Streamlit application
│   ├── agents.py       # AI Agents (Technical + Manager)
│   ├── database.py     # SQLite persistence module
│   └── .env            # Environment variables (API Key)
├── requirements.txt    # Project dependencies
└── industrial_predictions.db  # SQLite database
```

### AI Agents

| Agent | Role | Function |
|-------|------|----------|
| **Agent 1 - Technical Planner** | Geometric Analysis | Calculates XY grids, validates dimensions, generates structured JSON with layers and scrap |
| **Agent 2 - Optimization Manager** | Executive Report | Consolidates results, generates operator instructions, manages incidents |

## 🚀 Installation

### Prerequisites

- Python 3.8+
- An OpenAI API Key

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/jcm-developer/industrial-agents.git
   cd industrial-agents
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the `cuts/` folder:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

## ▶️ Usage

1. **Run the application**
   ```bash
   cd cuts
   streamlit run app.py
   ```

2. **Access the interface**
   
   Open in browser: `http://localhost:8501`

3. **Enter an industrial problem description**
   
   Input example:
   ```
   INVENTORY:
   - Blue Block: 6000mm x 200mm x 200mm
   - Red Block: 4000mm x 150mm x 150mm
   
   ORDERS:
   - Customer A: 50 blue pieces of 100mm x 50mm x 20mm
   - Customer B: 30 red pieces of 80mm x 40mm x 15mm
   ```

4. **View results**
   - Detailed technical analysis with Chain-of-Thought reasoning
   - Executive report for management
   - Graphical visualization of cutting plans

## 📦 Dependencies

| Package | Usage |
|---------|-------|
| `streamlit` | Web interface framework |
| `openai` | OpenAI API client |
| `pandas` | Tabular data handling |
| `python-dotenv` | Environment variable management |
| `matplotlib` | Chart generation |

## 🗄️ Database

The system uses SQLite to persist prediction history:

```sql
CREATE TABLE industrial_predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    client_req TEXT,           -- Order description
    first_review TEXT,         -- Agent 1 analysis
    second_review TEXT         -- Agent 2 report
);
```

## 🔧 Advanced Configuration

### Change AI model

In `agents.py`, modify the line:
```python
model="gpt-4o-mini"  # Change to "gpt-4o" for higher precision
```

### Adjust temperature

```python
temperature=0.2  # 0.0 = more deterministic, 1.0 = more creative
```

## 📄 License

This project is under the MIT License.

## 🤝 Contributing

Contributions are welcome. Please open an issue to discuss major changes before submitting a PR.

---

**Built with ❤️ using Streamlit + OpenAI**
