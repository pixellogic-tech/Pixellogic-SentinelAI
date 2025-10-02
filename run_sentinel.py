"""
SentinelAI Launcher
Prepared by Pixellogic
"""

from dashboard.main_dashboard import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
