import streamlit as st
from photos import get_couple_photos, get_date_photos, get_landscape_photos
from games import memory_game, heart_click_game, love_quiz
from utils import create_hearts_animation, display_photos_grid
# Page configuration
st.set_page_config(
    page_title="Our Love Journey",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)
# Custom CSS for a more lovey-dovey look
st.markdown("""
<style>
/* Custom scrollbar */
::-webkit-scrollbar {
    width: 12px;
}
::-webkit-scrollbar-track {
    background: #FFF0F5;
}
::-webkit-scrollbar-thumb {
    background: #FF5E8F; 
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
    background: #FF1493; 
}
/* Button styling */
.stButton button {
    border-radius: 30px !important;
    border: 2px solid #FF5E8F !important;
    transition: all 0.3s !important;
}
.stButton button:hover {
    transform: scale(1.03) !important;
    box-shadow: 0 5px 15px rgba(255, 94, 143, 0.4) !important;
}
/* Enhance success/info messages */
.stSuccess, .stInfo {
    border-radius: 15px !important;
    border: 2px dashed #FF5E8F !important;
}
</style>
""", unsafe_allow_html=True)
# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 0
if 'completed_games' not in st.session_state:
    st.session_state.completed_games = [False, False, False]
if 'show_confetti' not in st.session_state:
    st.session_state.show_confetti = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
# Navigation functions
def next_page():
    st.session_state.page += 1
    st.rerun()
def prev_page():
    st.session_state.page -= 1
    if st.session_state.page < 0:
        st.session_state.page = 0
    st.rerun()
def go_to_page(page_number):
    st.session_state.page = page_number
    st.rerun()
# Function to check if all games are completed
def check_all_completed():
    return all(st.session_state.completed_games)
# Main app logic
def main():
    # Get photos for different sections
    couple_photos = get_couple_photos()
    date_photos = get_date_photos()
    landscape_photos = get_landscape_photos()
    
    # Define significant dates and their descriptions
    memories = [
        {
            "date": "24th May to 6th June",
            "title": "The Farewell, The Triple Date Week, The Day We Got Together",
            "description": "Remember how we felt during those weeks, so excited, nervous but also happy. The cutest and most wholesome weeks. Our first kiss, cuddle all of it.",
            "photos": "C:\Users\KarteekPC\Downloads\WhatsApp Image 2025-05-17 at 17.03.14_a60602b1.jpg" + "C:\Users\KarteekPC\Downloads\WhatsApp Image 2025-05-17 at 17.03.00_fc35ed9c.jpg"
        },
        {
            "date": "August 10th and December 14th",
            "title": "The Nights We Spent.",
            "description": "August 10th was the day we said 'I love You' to each other, it's the most special day for me. These 2 days were the most beautiful and they were as heavenly as you are. The feeling of waking up beside you as you sleep holding me is something I'll never forget and that felt like we were stuck in time.",
            "photos": "C:\Users\KarteekPC\Downloads\WhatsApp Image 2025-05-17 at 17.13.52_4c8b968b.jpg" + "C:\Users\KarteekPC\Downloads\WhatsApp Image 2025-05-17 at 17.14.32_2205d932.jpg"
        },
        {
            "date": "June 29th and December 12th",
            "title": "Our Lunch Dates",
            "description": "Whether it was Ru or Apik, they were both abosultely beautiful. Our cute laughs and nervousness in Ru leading to us meeting after I came back in Apik and being full on couply. Every moment was loving.",
            "photos": "C:\Users\KarteekPC\Downloads\WhatsApp Image 2025-05-17 at 17.27.10_44253e08.jpg" + "C:\Users\KarteekPC\Downloads\WhatsApp Image 2025-05-17 at 17.38.08_96981aaa.jpg"
        }
    ]
    
    # Welcome page
    if st.session_state.page == 0:
        create_hearts_animation()
        
        st.markdown("<div class='page-title'><h1 style='text-align: center;'>✨ Our Love Journey ✨</h1></div>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>A celebration of our magical first year together 💖</h3>", unsafe_allow_html=True)
        
        # Warm welcome message
        st.markdown("""
        <div class='love-container'>
            <p class='love-text'>
                <span class='heartbeat'>💝</span> 
                Bangaram, thank you for the most wonderful year! 
                <span class='heartbeat'>💝</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Add a cute polaroid-style frame around the image
            st.markdown("""
            <style>
            .polaroid {
                background: #fff;
                padding: 15px 15px 40px;
                box-shadow: 0 8px 16px rgba(0,0,0,0.2);
                transform: rotate(-2deg);
                margin-bottom: 20px;
            }
            .polaroid img {
                width: 100%;
                height: auto;
                margin-bottom: 5px;
            }
            .polaroid p {
                text-align: center;
                font-family: 'Comic Sans MS', cursive;
                color: #FF5E8F;
                font-size: 18px;
                transform: rotate(2deg);
                margin: 0;
            }
            </style>
            <div class='polaroid'>
                <img src='""" + couple_photos[7] + """'>
                <p>Forever Yours</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <p style='text-align: center; font-size: 18px;'>
                Ready to relive our most precious moments together?
            </p>
            """, unsafe_allow_html=True)
            
            st.button("Begin Our Journey 💕", type="primary", on_click=next_page, use_container_width=True)
    # Memory pages with games
    elif 1 <= st.session_state.page <= 3:
        memory_index = st.session_state.page - 1
        memory = memories[memory_index]
        
        create_hearts_animation()  # Add floating hearts to every page
        
        # Pretty title with decorative elements
        st.markdown(f"""
        <div class='page-title'>
            <h1 style='text-align: center;'>
                <span style='display: inline-block; transform: rotate(-10deg); font-size: 24px;'>💖</span> 
                {memory['title']} 
                <span style='display: inline-block; transform: rotate(10deg); font-size: 24px;'>💖</span>
            </h1>
            <h3 style='text-align: center;'>{memory['date']}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Create a fancy container for the photos
        st.markdown("""
        <div class="love-container">
        """, unsafe_allow_html=True)
        
        # Display photos in a grid
        display_photos_grid(memory["photos"])
        
        # Close the container and show the description with styling
        st.markdown("""
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='love-text' style='margin-bottom: 20px;'>
            <span style='font-size: 24px;'>✨</span> {memory['description']} <span style='font-size: 24px;'>✨</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Make the divider prettier
        st.markdown("""
        <div style='text-align: center; margin: 20px 0;'>
            <span style='color: #FF5E8F; font-size: 20px;'>❤️💕❤️💕❤️</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Challenge title
        st.markdown("""
        <div style='text-align: center; margin-bottom: 20px;'>
            <h3 style='color: #FF5E8F; text-shadow: 1px 1px 3px rgba(255, 105, 180, 0.3);'>
                <span class='heartbeat'>💝</span> Sweet Challenge <span class='heartbeat'>💝</span>
            </h3>
            <p style='font-style: italic;'>Complete this little game to unlock our next memory!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Mini-games for each memory page
        if memory_index == 0:
            game_completed = memory_game(memory_index)
        elif memory_index == 1:
            game_completed = heart_click_game(memory_index)
        else:  # memory_index == 2
            game_completed = love_quiz(memory_index)
        
        # Update completion status
        if game_completed:
            st.session_state.completed_games[memory_index] = True
            
            # Add a little celebration on completion
            if not st.session_state.show_confetti:
                st.balloons()
                st.session_state.show_confetti = True
        else:
            st.session_state.show_confetti = False
        
        # Navigation buttons in cute containers
        st.markdown("<div style='padding: 20px 0; background: rgba(255, 240, 245, 0.5); border-radius: 15px; margin-top: 20px;'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.button("⬅️ Previous Page", on_click=prev_page, use_container_width=True)
        with col2:
            if st.session_state.completed_games[memory_index]:
                next_button_label = "Next Memory ➡️" if memory_index < 2 else "See My Surprise Gift ✨"
                st.button(next_button_label, type="primary", on_click=next_page, use_container_width=True)
            else:
                st.button("Complete the challenge to continue 💝", disabled=True, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
                
        # Fancy progress indicator
        st.markdown("""
        <div style='margin-top: 20px; text-align: center;'>
            <p style='margin-bottom: 10px; font-weight: bold; color: #FF5E8F;'>
                Our journey so far:
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Cute progress bar with hearts
        completed_count = st.session_state.completed_games.count(True)
        progress_cols = st.columns(7)
        for i in range(3):
            with progress_cols[i*2 + 1]:
                if st.session_state.completed_games[i]:
                    st.markdown(f"<p style='text-align: center; font-size: 20px;'>❤️</p>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p style='text-align: center; font-size: 20px;'>🤍</p>", unsafe_allow_html=True)
        
        with progress_cols[2]:
            st.markdown("<p style='text-align: center;'>→</p>", unsafe_allow_html=True)
        
        with progress_cols[4]:
            st.markdown("<p style='text-align: center;'>→</p>", unsafe_allow_html=True)
        
        # Text progress
        st.markdown(f"<p style='text-align: center; color: #FF5E8F; margin-top: 5px;'>{completed_count}/3 memories unlocked</p>", unsafe_allow_html=True)
    # Final video message page
    elif st.session_state.page == 4:
        if check_all_completed():
            st.balloons()
            
            # Create extra special hearts animation
            create_hearts_animation()
            
            # Add sparkly title with animation
            st.markdown("""
            <style>
            @keyframes sparkle {
              0% { text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 15px #FF5E8F, 0 0 20px #FF5E8F; }
              50% { text-shadow: 0 0 20px #fff, 0 0 30px #FF5E8F, 0 0 40px #FF5E8F, 0 0 50px #FF5E8F; }
              100% { text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 15px #FF5E8F, 0 0 20px #FF5E8F; }
            }
            .anniversary-title {
              animation: sparkle 2s infinite alternate;
              color: #FF5E8F;
              font-weight: bold;
              font-family: 'Comic Sans MS', cursive, sans-serif;
              text-align: center;
              padding: 20px 0;
              font-size: 2.5em;
            }
            .special-frame {
                background: linear-gradient(45deg, #FFD3DB, #FFABC4, #FFD3DB);
                border-radius: 20px;
                padding: 25px;
                box-shadow: 0 10px 30px rgba(255, 94, 143, 0.3);
                margin: 20px 0;
                border: 3px dashed #FF5E8F;
            }
            </style>
            <h1 class="anniversary-title">✨ Happy One Year Anniversary! ✨</h1>
            """, unsafe_allow_html=True)
            
            st.markdown("<h3 style='text-align: center;'>A special message just for you, my love</h3>", unsafe_allow_html=True)
            
            # Add cute animated emojis around the page
            st.markdown("""
            <div style="position: absolute; top: 20px; left: 20px; font-size: 30px; animation: heartbeat 1.5s infinite;">💖</div>
            <div style="position: absolute; top: 20px; right: 20px; font-size: 30px; animation: heartbeat 1.5s infinite;">💖</div>
            """, unsafe_allow_html=True)
            
            # Create a special frame for the video
            st.markdown("""
            <div class="special-frame">
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 3, 1])
            with col2:
                # Using a placeholder YouTube video
                st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
                
                # Add a personal message with decorative elements
                st.markdown(f"""
                <div style="text-align: center; margin: 20px 0; padding: 15px; background: rgba(255, 255, 255, 0.7); border-radius: 15px;">
                    <p style="font-family: 'Comic Sans MS', cursive; color: #FF5E8F; font-size: 18px; margin-bottom: 10px;">
                        <span style="font-size: 24px;">💌</span> My Dearest {st.session_state.user_name},
                    </p>
                    <p style="font-style: italic; margin-bottom: 15px;">
                        Thank you for being my everything. Every moment with you feels like a dream come true.
                        This past year has been the most beautiful chapter of my life, all because of your love.
                    </p>
                    <p style="font-weight: bold; color: #FF5E8F;">
                        Here's to many more beautiful years together! I love you to the moon and back!
                    </p>
                    <div style="font-size: 20px; margin-top: 10px;">
                        💝💕💖
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Add a cute button to start over
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown("<div style='text-align: center; margin-top: 20px;'>", unsafe_allow_html=True)
                st.button("💖 Relive Our Journey Again 💖", on_click=lambda: go_to_page(0), use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            # Create a gentle reminder to complete the challenges
            st.markdown("""
            <div style="text-align: center; padding: 30px; background: rgba(255, 240, 245, 0.8); border-radius: 20px; margin: 50px auto; max-width: 600px; box-shadow: 0 5px 15px rgba(255, 94, 143, 0.2); border: 2px dashed #FF5E8F;">
                <img src="https://pixabay.com/get/g792c60e17e8ce5d53dedc0ef4a5a6ee6f65ad9c3b767a70e6b87d5fbb70d6c81bc47e0fbc8979a9fd02cbd8efeeafed2f65bcac98c2ee17d6c7e1b0b4d9a6eb2_640.png" style="width: 100px; margin-bottom: 20px;">
                <h2 style="color: #FF5E8F; margin-bottom: 20px;">Just a little more to go!</h2>
                <p style="font-style: italic; margin-bottom: 20px;">Please complete all our special memory challenges first to unlock your surprise! 💝</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.button("Go Back to Continue Our Journey ❤️", on_click=prev_page, use_container_width=True)
if __name__ == "__main__":
    main()