# Jirathon: Inventory and Order Management System

This is a buggy Python/Flask project for the Jirathon event. Students will fix predefined bugs (see `BUGS.md`) as part of a project-based learning activity.

## Files
- `inventory_manager.py`: Handles inventory, users, orders, and analytics.
- `app.py`: Flask dashboard for viewing inventory and orders.
- `inventory.json`, `users.json`, `orders.json`, `logs.json`: Data persistence.
- `BUGS.md`: List of bugs to fix.

## Requirements

You need Python 3.8 or newer. Required packages:

```
Flask
Werkzeug
```

You can install them using:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install flask werkzeug
```

## How to Run

1. Clone this repository:
	```bash
	git clone https://github.com/finvediclabs/Advanced-Real-Time-Inventory-Management-System.git
	cd Advanced-Real-Time-Inventory-Management-System
	```
2. Install requirements:
	```bash
	pip install -r requirements.txt
	```
3. Start the Flask app:
	```bash
	python app.py
	```
4. Open your browser and go to `http://127.0.0.1:5000`

## Jirathon Instructions

- Clone the repo.
- Review `BUGS.md` for the list of bugs.
- Investigate and fix bugs in the codebase.
- Submit your fixes for review!