# ProxyPool Architect

Python 3.11+, FastAPI, और Redis के साथ बनाया गया एक आधुनिक, तेज़ और विश्वसनीय प्रॉक्सी पूल।

## विशेषताएँ
- **आधुनिक टेक स्टैक**: FastAPI, aiohttp, Redis, APScheduler, Loguru।
- **एसिंक्रोनस**: क्रॉलिंग से लेकर वैलिडेशन तक पूरी तरह से एसिंक्रोनस।
- **वेटेड स्कोरिंग**: गतिशील स्कोर-आधारित प्रबंधन (सफलता +10, विफलता -20)।
- **आसान परिनियोजन (Deployment)**: `uv` द्वारा प्रबंधित।

## त्वरित शुरुआत (Quick Start)

### 1. Redis इंस्टॉल करें (पूर्वापेक्षा)

#### macOS
```bash
brew install redis
brew services start redis
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
```

### 2. कॉन्फ़िगरेशन

यदि आवश्यक हो, तो डिफ़ॉल्ट सेटिंग्स को ओवरराइड करने के लिए रूट डायरेक्टरी में एक `.env` फ़ाइल बनाएं:
```env
REDIS_HOST=localhost
REDIS_PORT=6379
# REDIS_PASSWORD=your_password
```

### 3. प्रोजेक्ट इंस्टॉल करें और चलाएं
सुनिश्चित करें कि आपके पास `uv` इंस्टॉल है ([uv इंस्टॉल करें](https://docs.astral.sh/uv/getting-started/installation/))।

```bash
uv sync
uv run main.py
```

## API एंडपॉइंट्स
- `GET /get`: एक रैंडम उच्च-गुणवत्ता वाला प्रॉक्सी प्राप्त करें। `format=text` का समर्थन करता है।
- `GET /stats`: पूल की स्थिति और आंकड़े देखें।
- `GET /all`: पूल के सभी प्रॉक्सी की सूची देखें।

## इनके साथ निर्मित
![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)

---

## Docker के साथ परिनियोजन (Deployment)

यह प्रोजेक्ट Docker और Docker Compose के माध्यम से त्वरित परिनियोजन का समर्थन करता है।

### 1. Docker Compose का उपयोग करना (अनुशंसित)
यह सबसे आसान तरीका है, जो स्वचालित रूप से Redis और ProxyPool कंटेनर शुरू कर देता है:

```bash
docker-compose up -d
```

### 2. केवल ProxyPool इमेज बनाना
यदि आपके पास पहले से ही Redis चल रहा है:

```bash
# इमेज बनाएं
docker build -t proxy-pool .

# कंटेनर चलाएं (Redis एड्रेस निर्दिष्ट करें)
docker run -d -p 8000:8000 -e REDIS_HOST=host.docker.internal proxy-pool
```

---

## त्वरित उपयोग के उदाहरण

प्रॉक्सी प्राप्त करें और `curl` के साथ Google एक्सेस करें:

```bash
# 1. एक प्रॉक्सी प्राप्त करें (प्लेन टेक्स्ट फॉर्मेट)
PROXY=$(curl -s http://localhost:8000/get?format=text)

# 2. वेबसाइट एक्सेस करने के लिए उस प्रॉक्सी का उपयोग करें
curl -x "http://$PROXY" https://www.google.com -I
```

Python स्क्रिप्ट में उपयोग:

```python
import requests

# प्रॉक्सी प्राप्त करें
proxy = requests.get("http://localhost:8000/get?format=text").text

# प्रॉक्सी का उपयोग करें
proxies = {
    "http": f"http://{proxy}",
    "https": f"http://{proxy}",
}
response = requests.get("https://www.google.com", proxies=proxies)
print(response.status_code)
```


## मुख्य कार्य

- कई स्रोतों से स्वचालित रूप से प्रॉक्सी आईपी क्रॉल करना
- प्रॉक्सी आईपी की उपलब्धता और गति का रीयल-टाइम सत्यापन
- बैच प्रोसेसिंग और निर्धारित अपडेट के लिए समर्थन
- उपयोग में सरल और तैनात करने में त्वरित

## स्थापना और निष्पादन (Installation and Execution)

1. इस रिपॉजिटरी को क्लोन करें:

```
git clone https://github.com/XiaomingX/proxypool.git
cd proxypool
```

2. निर्भरताएँ (Dependencies) इंस्टॉल करें (Python वातावरण मानकर):

```
pip install -r requirements.txt
```

3. प्रॉक्सी क्रॉलिंग स्क्रिप्ट चलाएं:

```
python main.py
```

4. प्रॉक्सी सत्यापन स्क्रिप्ट चलाएं:

```
python verify.py
```

## साइबर सुरक्षा प्रोजेक्ट्स जो आपको पसंद आ सकते हैं:
 - Rust में कार्यान्वित पोर्ट स्कैनर:
   - https://github.com/XiaomingX/RustProxyHunter
 - Python में कार्यान्वित प्रॉक्सी पूल डिटेक्शन:
   - https://github.com/XiaomingX/proxy-pool
 - Golang में सप्लाई चेन सुरक्षा और CVE-POC स्वचालित संग्रह (नोट: कोई मैन्युअल समीक्षा नहीं):
   - https://github.com/XiaomingX/data-cve-poc
 - Python में कार्यान्वित .git लीक डिटेक्शन टूल:
   - https://github.com/XiaomingX/github-sensitive-hack

## संदर्भ और प्रेरणा

इस प्रोजेक्ट का डिज़ाइन और कार्यान्वयन निम्नलिखित उत्कृष्ट ओपन-सोर्स प्रोजेक्ट्स से प्रेरित था:

- [ProjectDiscovery Katana](https://github.com/projectdiscovery/katana) —— एक आधुनिक क्रॉलर और स्पाइडर फ्रेमवर्क।
- [Spider-rs Spider](https://github.com/spider-rs/spider) —— एक उच्च-प्रदर्शन, स्केलेबल क्रॉलर फ्रेमवर्क।

## योगदान मार्गदर्शिका

बेझिझक इश्यूज और पुल रिक्वेस्ट सबमिट करें ताकि हमें सुधार करने में मदद मिल सके।

## लाइसेंस

यह प्रोजेक्ट MIT लाइसेंस के तहत लाइसेंस प्राप्त है। विवरण के लिए LICENSE फ़ाइल देखें।

---

*ProxyPool का उपयोग करने का आनंद लें! यदि आपके कोई प्रश्न हैं, तो कृपया लेखक से संपर्क करें।*
