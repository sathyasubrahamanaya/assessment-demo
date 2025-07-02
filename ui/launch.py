#!/usr/bin/env python3
"""
Simple launcher for the AI Career Assessment Streamlit UI
"""

import subprocess
import sys
import os

def main():
    print("🎯 AI Career Assessment - Streamlit UI")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("streamlit_app.py"):
        print("❌ streamlit_app.py not found in current directory")
        print("💡 Make sure you're in the ui/ directory")
        return
    
    print("🚀 Starting Streamlit UI...")
    print("📱 The UI will open in your browser at: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 40)
    
    try:
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Streamlit UI stopped")
    except Exception as e:
        print(f"❌ Error starting Streamlit: {e}")

if __name__ == "__main__":
    main() 