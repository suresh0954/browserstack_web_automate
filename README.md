# browserstack_web_automate - Python + Selenium
Web Automate using Browserstack SDK

This project demonstrates cross-browser automated testing using **Selenium with BrowserStack Automate**, supporting both local and cloud testing workflows.

## 🧪 Features

- Parallel execution on Chrome (Windows) & Safari (macOS)
- Secure local testing via `browserstack-local`
- End-to-end cart flow simulation
- Session status reporting to BrowserStack dashboard
- Clean error handling & logs

---

## 🚀 Quick Start

### 1. Clone the Repo

```bash
git clone https://github.com/your-org/bs-automate-demo.git
cd bs-automate-demo/automate
```

### 2. Install Dependencies

Create a virtualenv and activate it:

```
python3 -m venv venv
source venv/bin/activate
```

Install packages:

```
pip install -r requirements.txt
```

### 3. Set Environment Variables

Create a .env file or export the variables in terminal:

```
export BROWSERSTACK_USERNAME="your_username"
export BROWSERSTACK_ACCESS_KEY="your_access_key"
export APP_USERNAME="dummy_username"
export APP_PASSWORD="dummy_password"
export BROWSERSTACK_PROJECT_NAME="bs-demo-cert"
export BROWSERSTACK_BUILD_NAME="Automate Build"
```

### 4. Run tests

```
python web_test.py
```

📦 File Structure

automate/
│
├── web_test.py            # Main web automation script
├── README.md              # You're here
├── requirements.txt       # All required Python packages
└── .env (optional)        # Environment variables (not committed)

🧠 Test Flow Summary

- Opens local app (http://localhost:3000)
- Selects username and password from dropdown
- Logs in
- Adds "iPhone 12" to cart
- Clicks checkout
- Marks test status (pass/fail) on BrowserStack dashboard

🛡️ Security Note

We're avoiding embedding credentials in URLs.
To further harden security, consider using ClientConfig in SDK-based flows (Optional - currently not supported in Selenium 4.x).

📎 Resources

BrowserStack Automate Docs
BrowserStack Local Testing
Selenium Python Docs
