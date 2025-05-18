import streamlit as st
import random
import time
from utils import create_hearts_animation

def memory_game(game_index):
    """
    A simple card matching memory game
    """
    st.markdown("""
    <div style="background-color: rgba(255, 238, 244, 0.7); padding: 15px; border-radius: 15px; border: 2px dashed #FF5E8F; margin-bottom: 20px;">
        <h4 style="text-align: center; color: #FF5E8F; margin-bottom: 10px;">💘 Love Memory Match 💘</h4>
        <p style="text-align: center; font-style: italic;">Find all the matching love symbols to unlock our next memory!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize game state if needed
    if f'memory_game_{game_index}' not in st.session_state:
        symbols = ['❤️', '💘', '💕', '💖', '💝', '💞', '💓', '💗']
        # Select 4 random symbols for 4 pairs
        selected_symbols = random.sample(symbols, 4)
        cards = selected_symbols + selected_symbols
        random.shuffle(cards)
        
        st.session_state[f'memory_game_{game_index}'] = {
            'cards': cards,
            'flipped': [False] * 8,
            'matched': [False] * 8,
            'selected': None,
            'attempts': 0,
            'complete': False,
            'match_animation': False,
            'match_time': None
        }
    
    game_state = st.session_state[f'memory_game_{game_index}']

    # --- OPTIONAL SKIP BUTTON ---
    if not game_state['complete']:
        if st.button("💫 Skip This Challenge", key=f"skip_{game_index}"):
            game_state['complete'] = True
            st.success("You skipped the challenge! Feel free to move forward 💖")
            return True
    
    # Skip rendering if already completed
    if game_state['complete']:
        st.markdown("""
        <div style="background-color: rgba(255, 234, 241, 0.9); padding: 20px; border-radius: 15px; text-align: center; border: 3px dotted #FF5E8F; margin: 20px 0;">
            <h3 style="color: #FF5E8F;">🎊 Challenge Completed! 🎊</h3>
            <p style="font-size: 18px;">You matched all the love symbols! Our hearts are in perfect harmony! 💖</p>
        </div>
        """, unsafe_allow_html=True)
        create_hearts_animation()
        return True
    
    # Check if we should clear the match animation
    if game_state['match_animation'] and time.time() - game_state['match_time'] > 1.5:
        game_state['match_animation'] = False
    
    # Add a cute card design
    st.markdown("""
    <style>
    .memory-card {
        background: linear-gradient(135deg, #FFB6C1, #FF69B4);
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        padding: 10px;
        margin: 5px;
        text-align: center;
        font-size: 24px;
        border: 2px solid #FFC0CB;
        transition: all 0.3s ease;
        min-height: 60px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .memory-card:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 16px rgba(255,105,180,0.3);
    }
    .memory-card.matched {
        background: linear-gradient(135deg, #FFD3DB, #FFA8C9);
        border: 2px solid #FF5E8F;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 94, 143, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(255, 94, 143, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 94, 143, 0); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Display cards in a grid
    st.markdown("<div style='background: rgba(255, 240, 250, 0.6); padding: 20px; border-radius: 15px; margin-bottom: 20px;'>", unsafe_allow_html=True)
    for row in range(2):
        cols = st.columns(4)
        for col in range(4):
            i = row * 4 + col
            # Determine card state
            if game_state['matched'][i]:
                card_class = "memory-card matched"
                card_display = game_state['cards'][i]
            elif game_state['flipped'][i]:
                card_class = "memory-card"
                card_display = game_state['cards'][i]
            else:
                card_class = "memory-card"
                card_display = "💌"  # Cute envelope for hidden cards
            
            # Custom card styling with HTML
            with cols[col]:
                st.markdown(f"""
                <div class="{card_class}" id="card_{game_index}_{i}">
                    {card_display}
                </div>
                """, unsafe_allow_html=True)
                
                # Hidden button for interaction (invisible)
                if st.button("", key=f"btn_{game_index}_{i}", 
                           help="Click to flip the card", 
                           disabled=game_state['matched'][i] or game_state['flipped'][i]):
                    # Card was clicked, handle logic
                    # If this is the first card of a pair
                    if game_state['selected'] is None:
                        game_state['selected'] = i
                        game_state['flipped'][i] = True
                    # If this is the second card
                    else:
                        # Check if it matches with first selection
                        first_selection = game_state['selected']
                        if game_state['cards'][first_selection] == game_state['cards'][i]:
                            # Match found!
                            game_state['matched'][first_selection] = True
                            game_state['matched'][i] = True
                            game_state['match_animation'] = True
                            game_state['match_time'] = time.time()
                        else:
                            # No match, flip back after a short delay
                            game_state['flipped'][i] = True
                            st.rerun()  # Show the second card briefly
                        
                        # Reset selection and increment attempts
                        game_state['flipped'] = [False if not game_state['matched'][j] else True for j in range(8)]
                        game_state['selected'] = None
                        game_state['attempts'] += 1
                        
                    # Check if game is complete
                    if all(game_state['matched']):
                        game_state['complete'] = True
                        st.success("Challenge completed! You matched all pairs! Our hearts are connected! 💖")
                        create_hearts_animation()
                        return True
                        
                    st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Show a fun message when a match is found
    if game_state['match_animation']:
        st.markdown("""
        <div style="text-align: center; margin: 10px 0; animation: heartbeat 1s infinite;">
            <span style="font-size: 24px; color: #FF5E8F;">💞 Perfect Match! 💞</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Display attempts counter with cute styling
    st.markdown(f"""
    <div style="text-align: center; padding: 10px; margin: 10px 0; background: rgba(255, 222, 234, 0.7); border-radius: 20px;">
        <p style="margin: 0; font-weight: bold; color: #FF5E8F;">
            <span style="font-size: 18px;">💭</span> Attempts: {game_state['attempts']} <span style="font-size: 18px;">💭</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Reset button with cute styling
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("✨ Shuffle Cards ✨", key=f"reset_memory_{game_index}"):
            symbols = ['❤️', '💘', '💕', '💖', '💝', '💞', '💓', '💗']
            # Select 4 random symbols for 4 pairs
            selected_symbols = random.sample(symbols, 4)
            cards = selected_symbols + selected_symbols
            random.shuffle(cards)
            
            game_state['cards'] = cards
            game_state['flipped'] = [False] * 8
            game_state['matched'] = [False] * 8
            game_state['selected'] = None
            game_state['attempts'] = 0
            game_state['match_animation'] = False
            st.rerun()
    
    return game_state['complete']

def heart_click_game(game_index):
    """
    A game where hearts must be clicked in the correct order
    """
    st.markdown("""
    <div style="background-color: rgba(255, 238, 244, 0.7); padding: 15px; border-radius: 15px; border: 2px dashed #FF5E8F; margin-bottom: 20px;">
        <h4 style="text-align: center; color: #FF5E8F; margin-bottom: 10px;">💘 Magic Love Hearts 💘</h4>
        <p style="text-align: center; font-style: italic;">Find and collect the hearts in order from 1 to 5 to unlock our next memory!</p>
        <p style="text-align: center; font-size: 12px;">Like our love journey, these hearts must be collected in the right order 💗</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize game state if needed
    if f'heart_game_{game_index}' not in st.session_state:
        st.session_state[f'heart_game_{game_index}'] = {
            'positions': list(range(5)),
            'current': 0,
            'complete': False,
            'mistake': False,
            'mistake_time': None,
            'success_time': None,
            'success_animation': False
        }
    
    game_state = st.session_state[f'heart_game_{game_index}']
    
    # Skip rendering if already completed
    if game_state['complete']:
        st.markdown("""
        <div style="background-color: rgba(255, 234, 241, 0.9); padding: 20px; border-radius: 15px; text-align: center; border: 3px dotted #FF5E8F; margin: 20px 0;">
            <h3 style="color: #FF5E8F;">🎊 Challenge Completed! 🎊</h3>
            <p style="font-size: 18px;">You've collected all the love hearts in perfect order! Just like our journey together! 💖</p>
        </div>
        """, unsafe_allow_html=True)
        create_hearts_animation()
        return True
    
    # Check if we need to reset the mistake message
    if game_state['mistake'] and time.time() - game_state['mistake_time'] > 1.5:
        game_state['mistake'] = False
        st.rerun()
    
    # Check if we need to clear the success animation
    if game_state['success_animation'] and time.time() - game_state['success_time'] > 1.5:
        game_state['success_animation'] = False
        st.rerun()
    
    # Add a cute heart design
    st.markdown("""
    <style>
    .heart-grid {
        background: linear-gradient(to bottom right, rgba(255, 240, 245, 0.7), rgba(255, 222, 234, 0.7));
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #FFC0CB;
        margin-bottom: 20px;
    }
    .heart-cell {
        width: 100%;
        height: 80px;
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 5px;
        border-radius: 15px;
    }
    .heart-button {
        background: linear-gradient(135deg, #FFB6C1, #FF69B4);
        border-radius: 50%;
        width: 60px;
        height: 60px;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 20px;
        box-shadow: 0 4px 8px rgba(255, 105, 180, 0.3);
        transition: all 0.3s ease;
        animation: float 3s ease-in-out infinite;
        cursor: pointer;
    }
    .heart-button:hover {
        transform: scale(1.1);
        box-shadow: 0 8px 16px rgba(255, 105, 180, 0.5);
    }
    .heart-collected {
        background: linear-gradient(135deg, #FFE4E1, #FFC0CB);
        animation: collected 1.5s infinite;
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    @keyframes collected {
        0% { box-shadow: 0 0 0 0 rgba(255, 105, 180, 0.7); }
        70% { box-shadow: 0 0 0 15px rgba(255, 105, 180, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 105, 180, 0); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Display hearts in a grid with random positions
    st.markdown("<div class='heart-grid'>", unsafe_allow_html=True)
    
    # Use a fixed seed for consistent layout
    random.seed(42 + game_index)
    positions = random.sample(range(15), 5)  # 15 positions, 5 hearts
    
    # Create 3x5 grid
    for row in range(3):
        cols = st.columns(5)
        for col in range(5):
            position = row * 5 + col
            
            with cols[col]:
                st.markdown(f"<div class='heart-cell'>", unsafe_allow_html=True)
                
                if position in positions:
                    heart_index = positions.index(position)
                    heart_num = heart_index + 1
                    
                    # Determine heart state and appearance
                    if heart_index < game_state['current']:
                        # Already collected heart
                        st.markdown(f"""
                        <div class='heart-button heart-collected'>
                            ✓
                        </div>
                        """, unsafe_allow_html=True)
                    elif heart_index == game_state['current']:
                        # Current target heart
                        if st.button(f"❤️ {heart_num}", key=f"heart_{game_index}_{position}", help=f"Heart {heart_num}"):
                            game_state['current'] += 1
                            game_state['success_animation'] = True
                            game_state['success_time'] = time.time()
                            
                            # Check if game completed
                            if game_state['current'] >= 5:
                                game_state['complete'] = True
                                return True
                            
                            st.rerun()
                    else:
                        # Future heart - clickable but results in error
                        if st.button(f"❤️ {heart_num}", key=f"heart_{game_index}_{position}", help=f"Heart {heart_num}"):
                            game_state['mistake'] = True
                            game_state['mistake_time'] = time.time()
                            st.error("Oops! Just like in love, we need to follow the right steps in order 💝")
                            st.rerun()
                else:
                    # Empty cell with some random decorations
                    if random.random() < 0.2:  # 20% chance to show a small decoration
                        decoration = random.choice(["✨", "🌸", "💫", "🌟", ""])
                        st.markdown(f"""
                        <div style="text-align: center; opacity: 0.5; font-size: 14px;">
                            {decoration}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.write("")
                
                st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Show a success message when a heart is collected
    if game_state['success_animation']:
        st.markdown(f"""
        <div style="text-align: center; margin: 10px 0; animation: heartbeat 1s infinite;">
            <span style="font-size: 24px; color: #FF5E8F;">💖 Heart {game_state['current']} Collected! 💖</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Show error message for wrong order
    if game_state['mistake']:
        st.markdown("""
        <div style="text-align: center; margin: 10px 0; color: #FF5E8F;">
            <p>Remember, true love follows a special path! 💖</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display progress with cute heart indicators
    st.markdown("<div style='margin: 20px 0;'>", unsafe_allow_html=True)
    cols = st.columns(5)
    
    for i in range(5):
        with cols[i]:
            if i < game_state['current']:
                st.markdown(f"<p style='text-align: center; font-size: 24px;'>❤️</p>", unsafe_allow_html=True)
            else:
                st.markdown(f"<p style='text-align: center; font-size: 24px;'>🤍</p>", unsafe_allow_html=True)
    
    # Display hearts collected text
    st.markdown(f"""
    <p style="text-align: center; color: #FF5E8F; margin-top: 10px; font-size: 16px;">
        {game_state['current']}/5 hearts collected
    </p>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Reset button with cute styling
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("💞 Start Over 💞", key=f"reset_heart_{game_index}"):
            game_state['current'] = 0
            game_state['mistake'] = False
            game_state['success_animation'] = False
            st.rerun()
    
    return game_state['complete']
    # --- OPTIONAL SKIP BUTTON ---
    if not game_state['complete']:
        if st.button("💫 Skip This Challenge", key=f"skip_{game_index}"):
            game_state['complete'] = True
            st.success("You skipped the challenge! Feel free to move forward 💖")
            return True


def love_quiz(game_index):
    """
    A simple quiz about romantic topics
    """
    st.markdown("""
    <div style="background-color: rgba(255, 238, 244, 0.7); padding: 15px; border-radius: 15px; border: 2px dashed #FF5E8F; margin-bottom: 20px;">
        <h4 style="text-align: center; color: #FF5E8F; margin-bottom: 10px;">💘 Sweet Love Quiz 💘</h4>
        <p style="text-align: center; font-style: italic;">Test your knowledge of love and romance to unlock our final memory!</p>
        <p style="text-align: center; font-size: 12px;">Each correct answer brings us one step closer to our special surprise 💗</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize game state if needed
    if f'quiz_game_{game_index}' not in st.session_state:
        st.session_state[f'quiz_game_{game_index}'] = {
            'questions': [
                {
                    'question': "What was the date we said 'I Love You' to each other?",
                    'options': ["June 1st", "July 11th", "August 2nd", "August 10th"],
                    'answer': 4,  # August 10th
                    'completed': True
                },
                {
                    'question': "What was the name of the restaurant we went to, when you gifted me the bracelet?",
                    'options': ["Ru", "Renao", "Dominos", "Chubby Cho"],
                    'answer': 2,  # Renao
                    'completed': True
                },
                {
                    'question': "What was my favorite date of ours?",
                    'options': ["Renao", "Dominos", "Last House", "Street Side Momos"],
                    'answer': 3,  # Last House
                    'completed': True
                }
            ],
            'current_question': 0,
            'complete': False,
            'wrong_answer': False,
            'wrong_time': None,
            'correct_answer': True,
            'correct_time': time.time()
        }
    
    game_state = st.session_state[f'quiz_game_{game_index}']
    
    # Skip rendering if already completed
    if game_state['complete']:
        st.markdown("""
        <div style="background-color: rgba(255, 234, 241, 0.9); padding: 20px; border-radius: 15px; text-align: center; border: 3px dotted #FF5E8F; margin: 20px 0;">
            <h3 style="color: #FF5E8F;">🎊 Quiz Completed! 🎊</h3>
            <p style="font-size: 18px;">You're a true love expert! Your heart is as wise as it is loving! 💖</p>
        </div>
        """, unsafe_allow_html=True)
        create_hearts_animation()
        return True
    
    # Clear temporary states
    if game_state['wrong_answer'] and time.time() - game_state['wrong_time'] > 2:
        game_state['wrong_answer'] = False
        st.rerun()
    if game_state['correct_answer'] and game_state['correct_time'] is not None and time.time() - game_state['correct_time'] > 2:
        game_state['correct_answer'] = False
        st.rerun()

    
    # Add cute quiz styling
    st.markdown("""
    <style>
    .quiz-card {
        background: linear-gradient(to bottom right, rgba(255, 245, 250, 0.9), rgba(255, 232, 242, 0.9));
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 5px 15px rgba(255, 105, 180, 0.15);
        border: 2px solid #FFC0CB;
        position: relative;
        overflow: hidden;
    }
    .quiz-card::before {
        content: "❤️";
        position: absolute;
        font-size: 60px;
        opacity: 0.05;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }
    .quiz-question {
        font-size: 20px;
        font-weight: bold;
        color: #FF5E8F;
        margin-bottom: 20px;
        text-align: center;
        padding: 10px;
        border-bottom: 2px dashed #FFD3DB;
    }
    .option-button {
        width: 100%;
        padding: 10px;
        margin: 8px 0;
        background: linear-gradient(135deg, #FFE4E1, #FFCAD4);
        border: 2px solid #FFCAD4;
        border-radius: 50px;
        text-align: center;
        font-size: 16px;
        color: #FF5E8F;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .option-button:hover {
        background: linear-gradient(135deg, #FFCAD4, #FFB6C1);
        transform: scale(1.03);
        box-shadow: 0 5px 10px rgba(255, 105, 180, 0.2);
    }
    .quiz-progress {
        margin-top: 20px;
        padding: 10px;
        background: rgba(255, 250, 252, 0.8);
        border-radius: 15px;
    }
    .heart-progress {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin: 10px 0;
    }
    .quiz-hearts {
        font-size: 24px;
    }
    .fun-fact {
        background-color: rgba(255, 245, 253, 0.8);
        border-left: 4px solid #FF5E8F;
        padding: 10px 15px;
        margin-top: 15px;
        border-radius: 0 10px 10px 0;
        font-style: italic;
        color: #8B4566;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Display decorative elements
    st.markdown("""
    <div style="text-align: center; margin-bottom: 15px;">
        <span style="font-size: 20px; color: #FF5E8F;">✨💕✨</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Display current question in a pretty card
    current = game_state['current_question']
    question = game_state['questions'][current]
    
    st.markdown("""
    <div class="quiz-card">
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="quiz-question">
        Question {current + 1}/{len(game_state['questions'])}: {question['question']}
    </div>
    """, unsafe_allow_html=True)
    
    # Display options with prettier buttons
    for i, option in enumerate(question['options']):
        if st.button(option, key=f"quiz_{game_index}_{current}_{i}", 
                   help=f"Select this answer", use_container_width=True):
            if i == question['answer']:
                # Correct answer
                question['completed'] = True
                game_state['correct_answer'] = True
                game_state['correct_time'] = time.time()
                
                # Display fun fact
                st.markdown(f"""
                <div class="fun-fact">
                    <span style="font-size: 18px;">💫</span> Fun Fact: {question['fun_fact']}
                </div>
                """, unsafe_allow_html=True)
                
                # Move to next question or complete quiz
                if current + 1 < len(game_state['questions']):
                    game_state['current_question'] += 1
                else:
                    game_state['complete'] = True
                    return True
                
                st.rerun()
            else:
                # Wrong answer
                game_state['wrong_answer'] = True
                game_state['wrong_time'] = time.time()
                st.error("That's not quite right. Try another answer! 💝")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Show celebration message on correct answer
    if game_state['correct_answer']:
        st.markdown("""
        <div style="text-align: center; margin: 15px 0; animation: heartbeat 1s infinite;">
            <span style="font-size: 24px; color: #FF5E8F;">💖 Correct! You're amazing! 💖</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Display progress with cute heart indicators
    completed_count = sum(q['completed'] for q in game_state['questions'])
    
    st.markdown("""
    <div class="quiz-progress">
        <p style="text-align: center; color: #FF5E8F; margin-bottom: 5px;">Your Love Knowledge:</p>
        <div class="heart-progress">
    """, unsafe_allow_html=True)
    
    # Display hearts for progress
    for i in range(len(game_state['questions'])):
        if i < completed_count:
            st.markdown(f"""<span class="quiz-hearts">❤️</span>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<span class="quiz-hearts">🤍</span>""", unsafe_allow_html=True)
    
    st.markdown("""
        </div>
        <p style="text-align: center; color: #FF5E8F; font-size: 14px; margin-top: 5px;">
            {}/3 questions answered
        </p>
    </div>
    """.format(completed_count), unsafe_allow_html=True)
    
    # Reset button with cute styling
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Start Quiz Over 🔄", key=f"reset_quiz_{game_index}"):
            for q in game_state['questions']:
                q['completed'] = False
            game_state['current_question'] = 0
            game_state['wrong_answer'] = False
            game_state['correct_answer'] = False

    # --- OPTIONAL SKIP BUTTON ---
    if not game_state['complete']:
        if st.button("💫 Skip This Challenge", key=f"skip_{game_index}"):
            game_state['complete'] = True
            st.success("You skipped the challenge! Feel free to move forward 💖")
            return True

