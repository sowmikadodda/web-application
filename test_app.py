"""
Test script to verify the AI-Powered Price Comparison Application
"""

import os
import sys

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import flask
        print("✅ Flask imported successfully")
    except ImportError:
        print("❌ Flask not found. Run: pip install flask")
        return False
    
    try:
        import tensorflow as tf
        print("✅ TensorFlow imported successfully")
        print(f"   TensorFlow version: {tf.__version__}")
    except ImportError:
        print("❌ TensorFlow not found. Run: pip install tensorflow")
        return False
    
    try:
        import cv2
        print("✅ OpenCV imported successfully")
    except ImportError:
        print("❌ OpenCV not found. Run: pip install opencv-python")
        return False
    
    try:
        import selenium
        print("✅ Selenium imported successfully")
    except ImportError:
        print("❌ Selenium not found. Run: pip install selenium")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("✅ BeautifulSoup imported successfully")
    except ImportError:
        print("❌ BeautifulSoup not found. Run: pip install beautifulsoup4")
        return False
    
    return True

def test_file_structure():
    """Test if all required files exist"""
    print("\n📁 Testing file structure...")
    
    required_files = [
        "app.py",
        "image_recognition.py", 
        "web_scraper.py",
        "requirements.txt",
        "templates/login.html",
        "templates/register.html",
        "templates/home.html",
        "templates/project.html",
        "static/style.css",
        "static/products"
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - Missing!")
            all_exist = False
    
    return all_exist

def test_ai_model():
    """Test if AI model can be loaded"""
    print("\n🤖 Testing AI model...")
    
    try:
        from image_recognition import ImageRecognizer
        recognizer = ImageRecognizer()
        print("✅ AI Image Recognition model loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Error loading AI model: {e}")
        return False

def main():
    print("🚀 AI-Powered Price Comparison Application - Test Suite")
    print("=" * 60)
    
    # Run tests
    imports_ok = test_imports()
    files_ok = test_file_structure()
    ai_ok = test_ai_model()
    
    print("\n" + "=" * 60)
    print("📊 Test Results:")
    print(f"   Imports: {'✅ PASS' if imports_ok else '❌ FAIL'}")
    print(f"   Files: {'✅ PASS' if files_ok else '❌ FAIL'}")
    print(f"   AI Model: {'✅ PASS' if ai_ok else '❌ FAIL'}")
    
    if imports_ok and files_ok and ai_ok:
        print("\n🎉 All tests passed! Ready to run the application.")
        print("\n🚀 To start the application:")
        print("   python app.py")
        print("\n🌐 Then open: http://localhost:5000")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        print("\n💡 Quick fixes:")
        print("   pip install -r requirements.txt")
        print("   python setup.py")

if __name__ == "__main__":
    main()