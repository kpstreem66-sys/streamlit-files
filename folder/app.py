import streamlit as st
import json
import os

st.title("Quiz Game")

questions_data = [
    {"q": "What is 2 + 2?", "a": "4"},
    {"q": "What is 400 * 2?", "a": "800"},
    {"q": "What is 10 - 7?", "a": "3"},
    {"q": "What is 5 * 5?", "a": "25"},
    {"q": "What is 12 / 3?", "a": "4"},
    {"q": "What is 15 + 9?", "a": "24"},
    {"q": "What is 20 - 11?", "a": "9"},
    {"q": "What is 7 * 6?", "a": "42"},
    {"q": "What is 64 / 8?", "a": "8"},
    {"q": "What is 50 + 50?", "a": "100"},
    {"q": "What is 11 * 11?", "a": "121"},
    {"q": "What is 100 - 45?", "a": "55"},
    {"q": "What is 9 * 9?", "a": "81"},
    {"q": "What is 36 / 6?", "a": "6"},
    {"q": "What is 14 + 14?", "a": "28"},
    {"q": "What is 8 * 5?", "a": "40"},
    {"q": "What is 70 - 25?", "a": "45"},
    {"q": "What is 13 + 17?", "a": "30"},
    {"q": "What is 45 / 9?", "a": "5"},
    {"q": "What is 12 * 4?", "a": "48"},
    {"q": "What is 100 / 4?", "a": "25"},
    {"q": "What is 33 + 67?", "a": "100"},
    {"q": "What is 85 - 30?", "a": "55"},
    {"q": "What is 6 * 8?", "a": "48"},
    {"q": "What is 15 * 3?", "a": "45"},
    {"q": "What is 90 / 10?", "a": "9"},
    {"q": "What is 18 + 22?", "a": "40"},
    {"q": "What is 60 - 15?", "a": "45"},
    {"q": "What is 7 * 7?", "a": "49"},
    {"q": "What is 150 / 3?", "a": "50"},
    {"q": "What is 25 * 4?", "a": "100"},
    {"q": "What is 200 - 85?", "a": "115"},
    {"q": "What is 14 * 2?", "a": "28"},
    {"q": "What is 81 / 9?", "a": "9"},
    {"q": "What is 45 + 55?", "a": "100"},
    {"q": "What is 12 * 5?", "a": "60"},
    {"q": "What is 130 - 40?", "a": "90"},
    {"q": "What is 72 / 8?", "a": "9"},
    {"q": "What is 16 + 16?", "a": "32"},
    {"q": "What is 3 * 15?", "a": "45"},
    {"q": "What is 400 / 4?", "a": "100"},
    {"q": "What is 19 + 11?", "a": "30"},
    {"q": "What is 95 - 25?", "a": "70"},
    {"q": "What is 12 * 12?", "a": "144"},
    {"q": "What is 50 / 2?", "a": "25"},
    {"q": "What is 65 + 35?", "a": "100"},
    {"q": "What is 150 - 75?", "a": "75"},
    {"q": "What is 8 * 9?", "a": "72"},
    {"q": "What is 120 / 6?", "a": "20"},
    {"q": "What is 30 * 3?", "a": "90"}
]

for idx, item in enumerate(questions_data):
    sub_key = f"sub_{idx}"
    ans_key = f"ans_{idx}"
    show_key = f"show_{idx}"
    
    if sub_key not in st.session_state:
        st.session_state[sub_key] = False
    if ans_key not in st.session_state:
        st.session_state[ans_key] = ""
    if show_key not in st.session_state:
        st.session_state[show_key] = False

    st.subheader(f"Question {idx + 1}")
    st.write(item["q"])

    with st.form(key=f"form_{idx}"):
        user_input = st.text_input("Your Answer:", value=st.session_state[ans_key], key=f"input_{idx}")
        submit_button = st.form_submit_button(label="Submit Answer")

        if submit_button:
            st.session_state[sub_key] = True
            st.session_state[ans_key] = user_input

    if st.button("Show Answer", key=f"btn_show_{idx}"):
        st.session_state[show_key] = not st.session_state[show_key]

    if st.session_state[show_key]:
        st.info(f"The correct answer is: {item['a']}")

    if st.session_state[sub_key]:
        cleaned = st.session_state[ans_key].strip()
        if cleaned == item["a"]:
            st.success("Correct! Well done.")
        elif cleaned == "":
            st.warning("Please enter an answer before submitting.")
        else:
            st.error(f"Incorrect. You answered '{cleaned}', but the correct answer is {item['a']}.")

    if (idx + 1) % 10 == 0:
        st.markdown("---")
        st.subheader(f"Milestone Mini-Game {int((idx + 1) / 10)}")
        game_click_key = f"game_click_{(idx + 1) // 10}"
        if game_click_key not in st.session_state:
            st.session_state[game_click_key] = 0
            
        if st.button("Click to score points!", key=f"game_btn_{(idx + 1) // 10}"):
            st.session_state[game_click_key] += 1
        st.write(f"Points scored: {st.session_state[game_click_key]}")
        st.markdown("---")

correct_count = 0
for idx, item in enumerate(questions_data):
    ans_key = f"ans_{idx}"
    if st.session_state[ans_key].strip() == item["a"]:
        correct_count += 1

if correct_count >= 10:
    st.balloons()
    st.header("Grand Finale Unlocked!")
    
    if "final_clicks" not in st.session_state:
        st.session_state.final_clicks = 0
        
    if st.button("CLICK TO CELEBRATE"):
        st.session_state.final_clicks += 1
        
    st.write(f"Celebration Click Score: {st.session_state.final_clicks}")

st.markdown("---")
st.subheader("Feedback and Comments")

comments_file = "comments.json"

if "comments_list" not in st.session_state:
    if os.path.exists(comments_file):
        try:
            with open(comments_file, "r") as f:
                st.session_state.comments_list = json.load(f)
        except:
            st.session_state.comments_list = []
    else:
        st.session_state.comments_list = []

with st.form(key="comment_form", clear_on_submit=True):
    new_comment = st.text_area("Leave a comment:")
    submit_comment = st.form_submit_button("Save Comment")
    
    if submit_comment and new_comment.strip() != "":
        st.session_state.comments_list.append(new_comment.strip())
        try:
            with open(comments_file, "w") as f:
                json.dump(st.session_state.comments_list, f)
        except:
            pass

if st.session_state.comments_list:
    st.write("Past Comments:")
    for c in st.session_state.comments_list:
        st.write(f"- {c}")

if any(st.session_state[f"sub_{i}"] for i in range(50)) and st.button("Reset Whole Quiz"):
    for i in range(50):
        st.session_state[f"sub_{i}"] = False
        st.session_state[f"ans_{i}"] = ""
        st.session_state[f"show_{i}"] = False
    for i in range(1, 6):
        st.session_state[f"game_click_{i}"] = 0
    st.session_state.final_clicks = 0
    st.rerun()
