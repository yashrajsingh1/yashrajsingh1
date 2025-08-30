# Mindware Solutions - AI Sales Assistant

## Overview
Mindware Solutions AI Sales Assistant is an advanced AI-powered chatbot designed to optimize the sales and support experience through both voice and text-based interactions. Built with OpenAI's GPT-4, it seamlessly engages customers, understands their needs, and offers personalized product recommendations.

The site is live - [Site_Link](https://ai-sales-bot-c4ks.onrender.com/)

## Features
- **Multi-Agent System:** Dedicated billing, sales, support, and technical agents for efficient query resolution.
- **Voice and Text Support:** Customers can interact via chat or voice calls, enhancing accessibility.
- **AI-Powered Conversations:** Uses OpenAI's GPT-4 to interact with users and guide them through the sales funnel.
- **Sales Stage Automation:** The AI follows a structured sales process, from introduction to closing the deal.
- **Product Recommendations:** Retrieves product information from a catalog and provides personalized suggestions.
- **Stripe Payment Integration:** Generates secure payment links for transactions.
- **Chat History Management:** Maintains a conversation history for contextual awareness.
- **Responsive Web Interface:** Provides a user-friendly chat interface.

## Project Structure
```
IT Product Sales Chatbot/
│── Agents/                     # Contains different agents handling various functionalities
│   │── billing_agent.py         # Handles billing-related queries
│   │── master_agent.py          # Main agent coordinating different tasks
│   │── sales_agent.py           # Manages sales interactions with customers
│   │── support_agent.py         # Provides customer support for IT products
│   │── technical_agent.py       # Assists with technical queries
│   │── tools.py                 # Utility functions used by agents
│
│── static/                      # Static assets (e.g., images, CSS, JavaScript)
│── templates/                   # HTML templates for chatbot UI
│── .gitignore                    # Files to ignore in version control
│── app.py                        # Main application script
│── app1.py                       # Additional application for voice call
│── call.py                       # Handles chatbot calls
│── Dockerfile                    # Configuration for containerization
│── product_catalog.json          # JSON file storing product details
│── README.md                     # Project documentation
│── requirements.txt              # Dependencies and libraries
│── save_products.py              # Script to save products into the database or storage

```

## Installation & Setup
### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Flask
- OpenAI API Key
- Stripe API Key
- TWILIO_ACCOUNT_SID
- TWILIO_AUTH_TOKEN
- Required Python libraries (see below)

### Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-repo/mindware-sales-bot.git
   cd mindware-sales-bot
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up API keys:**
   - Open `app.py` and replace the placeholders for OpenAI and Stripe API keys.
   ```python
   stripe.api_key = ""
   os.environ["OPENAI_API_KEY"] = ""
   ```
4. **Run the Flask application:**
   ```bash
   python app.py
   ```
5. **Access the application:**
   - Open a web browser and go to `http://127.0.0.1:5000/`

## Usage
- Start the chatbot and engage in a conversation.
- The AI will ask qualifying questions and recommend products.
- Once a purchase decision is made, the bot generates a Stripe payment link.
- Users can complete the payment via Stripe's secure gateway.

## API Endpoints
| Endpoint       | Method | Description  |
|---------------|--------|--------------|
| `/`           | GET    | Renders the chatbot UI |
| `/process`    | POST   | Processes user input and returns AI response |

## Technologies Used
- **Backend:** Flask, LangChain, OpenAI API, Python
- **Frontend:** HTML, CSS, JavaScript
- **Voice & Text Communication:** OpenAI Whisper, Twilio API
- **Payments:** Stripe API
- **Data Processing:** JSON, Python utilities
- **Deployment & Scalability:** Docker, FastAPI, Render

## Future Enhancements
- Integration with CRM for lead tracking
- Multi-language support
- Voice-based interaction
- Advanced analytics and user insights

## Contributing
Feel free to fork the repository and submit pull requests for improvements.

## Contact
For any queries, reach out to 1aryantyagi@gmail.com 
