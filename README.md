# 🛒 AI-Powered Price Comparison Application

An intelligent web application that uses AI image recognition to identify products from uploaded images and compares prices across multiple e-commerce platforms in real-time.

## 🌟 Features

- **🤖 AI Image Recognition**: Uses TensorFlow and MobileNetV2 to identify products from images
- **🔍 Real-time Price Scraping**: Automatically searches and compares prices from:
  - Amazon
  - Flipkart  
- **👤 User Authentication**: Secure login and registration system
- **📱 Responsive Design**: Works on desktop and mobile devices
- **🔗 Direct Store Links**: Click to view products on original store websites

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```

### 3. Open Browser
Navigate to `http://localhost:5000`

## 📋 Requirements

- Python 3.7+
- Flask
- TensorFlow
- OpenCV
- Selenium
- BeautifulSoup4
- Chrome Browser (for web scraping)

## 🎯 How It Works

1. **Upload Image**: Users upload a product image (JPG, PNG, JPEG)
2. **AI Recognition**: TensorFlow model identifies the product category
3. **Price Scraping**: Selenium and BeautifulSoup scrape real prices from stores
4. **Comparison**: Display prices with direct links to purchase

## 🛠️ Technical Architecture

```
├── app.py                 # Main Flask application
├── image_recognition.py   # AI image recognition module
├── web_scraper.py        # Web scraping for price comparison
├── templates/            # HTML templates
├── static/              # CSS, JS, uploaded images
└── users.db            # SQLite database
```

## 🔧 Configuration

### Image Recognition
- Uses pre-trained MobileNetV2 model
- Supports common product categories
- Confidence threshold: 0.1

### Web Scraping
- Headless Chrome browser
- Rotating user agents
- Error handling and fallbacks

## 📸 Supported Products

- 📱 Smartphones
- 💻 Laptops
- 📷 Cameras
- ⌚ Smartwatches
- 🎧 Headphones
- And more...

## 🚨 Important Notes

1. **Web Scraping**: Respects robots.txt and implements delays
2. **Rate Limiting**: Built-in delays to avoid overwhelming servers
3. **Error Handling**: Graceful fallbacks when scraping fails
4. **Privacy**: Images are stored locally and can be deleted

## 🔒 Security Features

- Password hashing with Werkzeug
- Session management
- File upload validation
- SQL injection protection

## 🐛 Troubleshooting

### Common Issues:

1. **Chrome Driver Error**: Install Chrome browser and update chromedriver
2. **TensorFlow Issues**: Ensure compatible Python version (3.7-3.9)
3. **Scraping Blocked**: Some sites may block automated requests

### Solutions:
```bash
# Update Chrome driver
pip install --upgrade webdriver-manager

# Install TensorFlow CPU version
pip install tensorflow-cpu

# Clear browser cache if scraping fails
```

## 📈 Future Enhancements

- [ ] More e-commerce platforms
- [ ] Price history tracking
- [ ] Email alerts for price drops
- [ ] Mobile app version
- [ ] Advanced product matching
- [ ] User wishlist feature

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License

This project is for educational purposes. Please respect the terms of service of e-commerce websites when scraping.

## 🙏 Acknowledgments

- TensorFlow team for pre-trained models
- Flask community for excellent documentation
- E-commerce platforms for providing public data

---

**⚠️ Disclaimer**: This application is for educational purposes. Always respect website terms of service and implement appropriate delays when scraping.