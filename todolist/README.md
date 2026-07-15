# TaskFlow Pro — Smart Todo Management System

TaskFlow Pro is a modern, production-grade Todo List SaaS web application built with **Python**, **Streamlit**, and a safe local **JSON Database** layer. It includes multi-user isolation, bcrypt password hashing, dynamic glassmorphic styles, interactive analytics, and robust history recovery mechanisms.

## 🚀 Features

- **Secure Multi-User Auth**: Login, registration, and logout flows backed by secure `bcrypt` salt/hashing.
- **Modern Responsive SaaS UI**: Clean Poppins/Inter typography, soft dark navy styles, responsive grids, collapsible sidebars, and customizable theme settings (Light and Dark mode toggles).
- **Stat Cards**: Dynamic dashboards displaying Total, Completed, Pending, and Deleted task counts along with completion ratios.
- **Interactive Analytics**: Embedded Plotly donut and pie charts summarizing priority distributions and category counts.
- **Advanced Task Operations**: Search, filter, and sort tasks dynamically by category, priority, status, or due date.
- **Safe soft-deletes & Recovery**: Deleting active tasks routes them to a dedicated history list from which they can be restored or permanently removed.
- **Robust Data Layer**: Atomic write structures prevent JSON database corruption during concurrent operations.
- **Inactivity Timeout**: Log users out automatically after 30 minutes of session inactivity.

---

## 📂 Project Structure

```text
TodoList/
│
├── app.py                     # Main router & Entrypoint
├── requirements.txt           # Python dependency declarations
├── README.md                  # Project documentation
│
├── .streamlit/
│   └── config.toml            # Custom dark navy theme configuration
│
├── database/
│   ├── users.json             # User accounts record
│   ├── tasks.json             # Task records per user
│   ├── history.json           # Soft deleted tasks
│   └── settings.json          # User settings (theme toggles)
│
├── pages/
│   ├── login.py               # Auth login screen
│   ├── register.py            # User registration screen
│   ├── dashboard.py           # Dashboard list, form, and analytics
│   ├── history.py             # Completed and soft deleted tasks history
│   └── profile.py             # User stats and settings
│
├── components/
│   ├── navbar.py              # Header navbar layout
│   ├── sidebar.py             # Option menu navigation panel
│   ├── cards.py               # Dashboard stats cards
│   ├── forms.py               # Create/Edit form handlers
│   ├── tables.py              # Interactive task table grid
│   ├── statistics.py          # Plotly analytical dashboards
│   ├── modals.py              # Confirmation popup controls
│   ├── buttons.py             # Styled buttons
│   └── footer.py              # Branding footnotes
│
├── styles/
│   ├── style.css              # Custom SaaS style overrides
│   ├── theme.py               # Compiler and dynamic theme swaps
│   └── animations.py          # Keyframe animation styles
│
└── utils/
    ├── auth.py                # bcrypt hash matching operations
    ├── database.py            # Atomic JSON load/save operations
    ├── validation.py          # Regex and length validators
    ├── session.py             # Session initialization and timeout
    ├── helpers.py             # Human-friendly dates and string limiters
    ├── constants.py           # Global dropdown items and color hexes
    ├── security.py            # HTML sanitizers against XSS injections
    └── logger.py              # Logging warning/error file wrapper
```

---

## 💻 Local Setup & Installation

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd TodoList
   ```

2. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the local Streamlit application**:
   ```bash
   streamlit run app.py
   ```

---

## 🌐 Render Deployment

To deploy TaskFlow Pro to Render, you can connect your GitHub repository and link using the included `render.yaml` configuration.
- **Environment**: Python
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
