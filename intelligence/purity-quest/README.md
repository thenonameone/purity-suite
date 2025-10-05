# 🫁 Purity Quest - PURITY IS KEY

**Digital Life Support OSINT Tool with GUI Interface**

A comprehensive OSINT (Open Source Intelligence) investigation tool with a dark-themed graphical user interface, featuring phone number and email address investigation capabilities.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)

## 🚀 Features

### 📱 Phone Number Investigation
- **Real-time API validation** with Twilio and IPQualityScore
- **Carrier identification** and line type detection
- **Location information** (city, region, country)
- **Fraud score analysis**
- **Live web search results** via SerpAPI
- **Comprehensive search query generation**

### 📧 Email Address Investigation
- **Email deliverability testing** with Hunter.io
- **Data breach detection** via Have I Been Pwned API
- **SMTP validation** and provider identification
- **Disposable email detection**
- **Social media profile searches**
- **Professional background investigation**

### 🚨 Combined Investigation
- **Cross-reference email and phone data**
- **Synchronized investigation protocols**
- **Dual patient resuscitation mode**
- **Comprehensive results correlation**

### 🔑 Built-in API Management
- **Intuitive API key configuration** with GUI input fields
- **"Seek the Warm Embrace"** button to open all signup sites
- **Real-time API connectivity testing**
- **Automatic configuration persistence**

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- tkinter (usually included with Python)
- Linux environment (tested on Kali Linux)

### Quick Setup
1. Clone the repository:
```bash
git clone https://github.com/yourusername/purity-quest.git
cd purity-quest
```

2. Install required dependencies:
```bash
pip install requests
```

3. Make the script executable:
```bash
chmod +x Purity_Quest.py
```

4. Run the application:
```bash
python3 Purity_Quest.py
```

### Optional: System-wide Command
To run with the custom `make me pure` command:

1. Copy the launcher script to your PATH:
```bash
sudo cp Purity_Quest.py /usr/local/bin/purity-quest
```

2. Create an alias (add to ~/.zshrc or ~/.bashrc):
```bash
echo 'alias "make me pure"="python3 /usr/local/bin/purity-quest"' >> ~/.zshrc
source ~/.zshrc
```

## 🔧 API Configuration

The tool supports multiple APIs for enhanced investigation capabilities:

### Free APIs (Recommended for beginners)
- **SerpAPI**: 100 searches/month - [Sign up here](https://serpapi.com/)
- **IPQualityScore**: 5,000 requests/month - [Sign up here](https://www.ipqualityscore.com/)
- **Hunter.io**: 100 email verifications/month - [Sign up here](https://hunter.io/)

### Paid APIs (Advanced features)
- **Have I Been Pwned**: $3.50/month - [Subscribe here](https://haveibeenpwned.com/API/v3)
- **Twilio**: Pay-per-use - [Sign up here](https://www.twilio.com/)

### Configuration Methods

#### Method 1: GUI Configuration (Recommended)
1. Launch the application
2. Go to the "🔑 API Keys" tab
3. Click "🤗 Seek the Warm Embrace" to open signup sites
4. Enter your API keys and click "💾 Save API Keys"
5. Use "✅ Test APIs" to verify connectivity

#### Method 2: Environment Variables
```bash
export SERPAPI_KEY="your_serpapi_key"
export IPQS_API_KEY="your_ipqs_key"
export HUNTER_API_KEY="your_hunter_key"
export HIBP_API_KEY="your_hibp_key"
export TWILIO_ACCOUNT_SID="your_twilio_sid"
export TWILIO_AUTH_TOKEN="your_twilio_token"
```

## 📖 Usage

### GUI Interface
The application features a tabbed interface with:

1. **📱 Phone CPR**: Phone number investigation
2. **📧 Email Life Support**: Email address investigation  
3. **🚨 Emergency CPR**: Combined investigation
4. **⚙️ API Settings**: Configuration status
5. **🔑 API Keys**: Key management and configuration

### Investigation Examples

#### Phone Number Investigation
- Enter any phone number format (e.g., 555-123-4567, +1-555-123-4567)
- Get carrier information, location data, and fraud scores
- Receive comprehensive search queries for manual investigation
- View live search results (with SerpAPI configured)

#### Email Investigation
- Enter any email address
- Check deliverability and SMTP validity
- Detect if email appears in data breaches
- Get social media and professional search queries

## 🎨 Interface Features

- **Medical/CPR Theme**: Emergency response aesthetic
- **Dark Theme**: Red and black color scheme
- **Large, Readable Fonts**: Optimized for accessibility
- **Responsive Layout**: Adapts to different screen sizes
- **Progress Indicators**: Real-time investigation updates

## 🛡️ Privacy & Security

- **No data storage**: All investigations are performed in real-time
- **API key encryption**: Keys are masked in the interface
- **Local processing**: No data sent to third parties except configured APIs
- **Open source**: Full transparency of operations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📋 Requirements

```
requests>=2.25.0
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and legitimate investigation purposes only. Users are responsible for complying with applicable laws and API terms of service. Always obtain proper authorization before investigating individuals or organizations.

## 🙏 Acknowledgments

- Built with Python and tkinter
- Inspired by digital forensics and OSINT methodologies
- Medical/CPR theme represents "reviving" digital information
- Special thanks to the open source intelligence community

## 📞 Support

If you encounter issues or have questions:
- Open an issue on GitHub
- Check the API configuration in the GUI
- Verify API keys are correctly entered
- Ensure all dependencies are installed

---

**"When data flatlines, we revive it"** 🫁

*Purity Quest - Where every bit deserves a second chance*