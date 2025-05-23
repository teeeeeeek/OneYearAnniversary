# utils.py
import streamlit as st

def create_hearts_animation():
    st.markdown("""
    <style>
    @keyframes float {
        0% {
            transform: translateY(0px);
            opacity: 1;
        }
        100% {
            transform: translateY(-100vh);
            opacity: 0;
        }
    }
    
    .floating-heart {
        position: fixed;
        bottom: -50px;
        font-size: 24px;
        animation: float 10s linear infinite;
        color: #FF69B4;
        opacity: 0.8;
    }
    
    .heart1 { left: 10%; animation-delay: 0s; }
    .heart2 { left: 25%; animation-delay: 2s; }
    .heart3 { left: 40%; animation-delay: 4s; }
    .heart4 { left: 55%; animation-delay: 1s; }
    .heart5 { left: 70%; animation-delay: 3s; }
    .heart6 { left: 85%; animation-delay: 5s; }
    </style>

    <div class="floating-heart heart1">💖</div>
    <div class="floating-heart heart2">💕</div>
    <div class="floating-heart heart3">💗</div>
    <div class="floating-heart heart4">💓</div>
    <div class="floating-heart heart5">💞</div>
    <div class="floating-heart heart6">💘</div>
    """, unsafe_allow_html=True)

def display_photos_grid(photo_paths):
    import streamlit as st

    cols = st.columns(2)
    for i, path in enumerate(photo_paths):
        with cols[i % 2]:
            st.markdown(
                f"""
                <div style="text-align: center; padding: 10px;">
                    <img src="{path}" style="
                        width: 280px;
                        height: 370px;
                        object-fit: cover;
                        border-radius: 15px;
                        border: 2px solid #FFB6C1;
                        box-shadow: 0 4px 12px rgba(255, 182, 193, 0.3);
                    " alt="memory">
                </div>
                """,
                unsafe_allow_html=True
            )
