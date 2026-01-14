"""
Sorted - File Auto-Organizer
Entry point for the application with PyWebView
"""

import sys
import webview
from pathlib import Path
from threading import Thread
from backend.server import create_app

# Get project root
PROJECT_ROOT = Path(__file__).parent

def run_server():
    """Run Flask server in background"""
    app = create_app()
    app.run(debug=False, host="127.0.0.1", port=5000, use_reloader=False)

def main():
    """Launch PyWebView with Flask backend"""
    
    # Start Flask server in background thread
    server_thread = Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Create and show web view
    webview.create_window(
        title="Sorted - File Auto-Organizer",
        url="http://127.0.0.1:5000",
        width=1000,
        height=700,
        min_size=(800, 600),
    )
    
    webview.start(debug=False)

if __name__ == "__main__":
    main()
