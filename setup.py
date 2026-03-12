"""
AI-Powered Price Comparison Application Setup
============================================

This script helps set up the application with all required dependencies.
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Error installing packages. Please install manually:")
        print("pip install -r requirements.txt")

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    directories = [
        "static/products",
        "templates"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created: {directory}")

def main():
    print("🚀 Setting up AI-Powered Price Comparison Application...")
    print("=" * 50)
    
    create_directories()
    install_requirements()
    
    print("\n🎉 Setup completed!")
    print("\n📋 To run the application:")
    print("1. python app.py")
    print("2. Open browser to http://localhost:5000")
    print("\n🔍 Features:")
    print("• AI-powered image recognition")
    print("• Real-time price scraping from Amazon, Flipkart, Walmart")
    print("• User authentication")
    print("• Responsive web interface")

if __name__ == "__main__":
    main()