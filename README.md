img[]
# 🚀 Deteflect Framework

An intelligent **Natural Language Processing (NLP)** framework designed to discover user intentions, analyze sentiment, extract entities, and execute custom rules based on natural language input. Built with Flask and PyTorch, Deteflect provides a powerful API for understanding and responding to user prompts with contextual awareness.

---

## 📋 Table of Contents

- [What is Deteflect?](#what-is-deteflect)
- [Project Setup](#project-setup)
- [Project Documentation](#project-documentation)
- [API Routes](#api-routes)
- [Browser Usage](#browser-usage)
- [Contributing](#contributing)

---

## 🤖 What is Deteflect?

Deteflect is an intelligent intention discovery system that processes natural language input to:

- **Detect User Intentions** - Automatically identify what users are trying to accomplish
- **Analyze Sentiment** - Understand the emotional tone and sentiment of messages
- **Extract Entities** - Identify important objects, people, and concepts mentioned
- **Correct Syntax** - Automatically fix spelling and grammar errors
- **Extract Keywords** - Find the most relevant keywords and key phrases
- **Execute Custom Rules** - Trigger predefined actions based on pattern matching

The framework combines advanced NLP models with PyTorch-powered deep learning and a flexible rule engine, making it ideal for:
- Chatbot development
- Customer service automation
- Intent-based automation systems
- Natural language analysis pipelines

---

## ⚙️ Project Setup

### Prerequisites

Before you begin, ensure you have the following installed on your machine:

- **Python 3.8+** (Latest stable version recommended)
- **pip** (Python package manager, comes with Python)
- **Git** (for cloning the repository)

### Installation Steps

#### 1. **Clone or Download the Project**

```bash
# If using Git
git clone <repository-url>
cd DescobrirIntent
```

#### 2. **Navigate to Project Directory**

```bash
cd Dataflect
```

#### 3. **Create a Virtual Environment** (Recommended)

Creating a virtual environment isolates project dependencies:

```bash
# On Windows (PowerShell or CMD)
python -m venv env

# Activate the virtual environment
# On Windows (Command Prompt)
env\Scripts\activate

# On Windows (PowerShell)
.\env\Scripts\Activate.ps1

# On macOS/Linux
source env/bin/activate
```

You should see `(env)` in your terminal prompt when activated.

#### 4. **Install Dependencies**

Install all required packages from the requirements file:

```bash
pip install -r requirements.txt
```

This will install:
- **Flask** - Web framework
- **PyTorch** - Deep learning framework
- **spaCy** - NLP library
- **Flask-CORS** - Cross-Origin Resource Sharing support
- And all other dependencies

#### 5. **Download NLP Models** (First Time Only)

```bash
# Navigate to the setup scripts folder
cd script

# Run the spaCy setup script
python setup_spacy.py

# Go back to the main folder
cd ..
```

This downloads the pre-trained spaCy language models needed for NLP processing.

### Running the Application

#### **Start the Development Server**

```bash
# Make sure you're in the Dataflect directory and virtual environment is activated
python app.py
```

Expected output:
```
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with reloader
```

#### **Access the Web Interface**

Open your browser and navigate to:
```
http://localhost:5000
```

You should see the Deteflect welcome screen and input box.

---

## 📚 Project Documentation

### Project Structure Overview

```
Dataflect/
├── app.py                    # Flask application entry point
├── project.py                # Custom rules configuration
├── requirements.txt          # Project dependencies
├── controller/               # Business logic controllers
├── routes/                   # API route blueprints
├── rules/                    # Custom rules engine
├── nlp/                      # NLP models and processing
│   ├── facade.py            # NLP interface
│   ├── torch_pipeline.py    # PyTorch processing
│   └── model/               # Neural network models
└── pipeline/                # Data processing pipelines
```

### Configuring project.py - Custom Rules

The `project.py` file is where you define custom rules that trigger based on user input patterns.

#### **Understanding Rules**

Rules work by matching keywords in user input and executing associated functions. Each rule consists of:

1. **Trigger Keywords** - What to look for (tuple of strings)
2. **Rule Type** - Type of rule (`"READ"`, `"EXECUTE"`, etc.)
3. **Action Function** - Function to call when rule is triggered

#### **Creating Custom Rules - Step by Step**

**Step 1: Import the Rules Engine**

```python
from rules.RulesUser import RulesSintaxe

# Initialize the rules system
Rule_data = RulesSintaxe()
```

**Step 2: Define Data for Your Rules**

```python
# Example: Define a shopping list
list_mercado = ["pera", "maca", "banana", "limao"]

# You can add any other data your rules need
user_preferences = {
    "color": "blue",
    "language": "portuguese"
}
```

**Step 3: Create Action Functions**

These functions execute when a rule is triggered:

```python
def Mostrar_list():
    """Function executed when shopping rule is triggered"""
    return f"These are the items I need to buy at the market: {list_mercado}"

def Get_preference(key):
    """Function to retrieve user preferences"""
    return user_preferences.get(key, "Not found")

def Custom_action():
    """Add your custom logic here"""
    return "Your custom response here"
```

**Step 4: Register Rules**

Use the `NewRule()` method to register rules:

```python
# Syntax: Rule_data.NewRule(keywords, rule_type, action_function)

# Rule for shopping list
Rule_data.NewRule(("comprar", "produtos"), "READ", Mostrar_list)
Rule_data.NewRule(("compras", "produtos"), "READ", Mostrar_list)
Rule_data.NewRule(("mercado", "lista"), "READ", Mostrar_list)

# Rule for preferences
Rule_data.NewRule(("preferencia", "cor"), "READ", lambda: Get_preference("color"))

# Rule for custom actions
Rule_data.NewRule(("acao", "customizada"), "EXECUTE", Custom_action)
```

#### **How Rules Work**

1. User sends a message through the browser
2. System extracts keywords from the message
3. Keywords are compared against registered rules
4. If a match is found, the associated function is executed
5. Response is returned to the user

#### **Advanced Rule Configuration**

```python
# Add multiple keywords to create more flexible rules
Rule_data.NewRule(("quero", "quer", "desejo"), "READ", action_function)

# Rules support case-insensitive matching automatically
# "COMPRAR produtos" will match "comprar produtos" rule

# Memory-based rules for remembering context
Rule_data.MemoryData("previous_user_input", "associated_rule")

# Retrieve memory
rule = Rule_data.GetMemory("previous_user_input")
```

---

### Using Deteflect in the Browser

The web interface provides a simple way to interact with Deteflect without writing code.

#### **Accessing the Interface**

1. **Start the application** (see "Running the Application" section)
2. **Open your browser** to `http://localhost:5000`

#### **Browser Interface Features**

The Deteflect browser interface includes:

- **Welcome Message** - Initial greeting and instructions
- **Input Field** - Text box for entering your messages
- **Send Button** - Submit your message for analysis
- **Response Display** - Results showing:
  - **Intent** - What the user is trying to do
  - **Keywords** - Most relevant words and phrases
  - **Entities** - Important objects and concepts identified
  - **Sentiment** - Emotional tone (positive, negative, neutral)
  - **Rule Triggers** - Any custom rules that were activated

#### **Example Usage**

1. **Type in the input box:**
   ```
   I need to buy pears, apples, and bananas at the market
   ```

2. **Click Send** button or press Enter

3. **View the analysis:**
   - Intent: Shopping/Purchase
   - Keywords: buy, market, fruits
   - Entities: pears, apples, bananas, market
   - Sentiment: Neutral/Positive
   - Rules Triggered: Shopping list rule (if configured)

#### **Tips for Best Results**

- ✅ Use clear, grammatically correct sentences for better accuracy
- ✅ Include relevant context in your messages
- ✅ Use specific keywords that match your configured rules
- ✅ If not understood, rephrase and try again
- ✅ The system corrects minor spelling mistakes automatically

---

## 🔌 API Routes

### Analyze Message via API

**Endpoint:**
```
GET /sendmensage/API/<text>
```

**Example:**
```
http://localhost:5000/sendmensage/API/I%20want%20to%20buy%20fruits
```

**Response Format:**
```json
{
  "Response": {
    "intent": "shopping",
    "MajorKeywords": ["buy", "fruits"],
    "Entities": ["fruits"],
    "Sentiment": "neutral"
  }
}
```

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the terms specified in the LICENSE file.

---

## 👤 Author

Created by Felipe Katao - 2026 - All rights reserved

---

## 📞 Support

For issues, questions, or suggestions, please open an issue on the project repository.

**Happy Analyzing! 🎉**




