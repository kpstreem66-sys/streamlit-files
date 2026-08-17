import streamlit as st

st.title("Quiz Game")

questions_data = [
    {"q": "What is 2 + 2?", "a": "4"},
    {"q": "What is 400x2?", "a": "800"},
    {"q": "What is 10 - 7?", "a": "3"},
    {"q": "What is 5x5?", "a": "25"},
    {"q": "What is 12 / 3?", "a": "4"},
    {"q": "What is 15 + 9?", "a": "24"},
    {"q": "What is 20 - 11?", "a": "9"},
    {"q": "What is 7x6?", "a": "42"},
    {"q": "What is 64 / 8?", "a": "8"},
    {"q": "What is 9x9?", "a": "81"},
    {"q": "What is 50x2?", "a": "100"},
    {"q": "What is 100 - 45?", "a": "55"}
]

for idx, item in enumerate(questions_data, start=1):
    sub_key = f"q{idx}_submitted"
    ans_key = f"q{idx}_user_answer"
    show_key = f"q{idx}_show_answer"

    if sub_key not in st.session_state:
        st.session_state[sub_key] = False
    if ans_key not in st.session_state:
        st.session_state[ans_key] = ""
    if show_key not in st.session_state:
        st.session_state[show_key] = False

correct_count = 0
for idx, item in enumerate(questions_data, start=1):
    sub_key = f"q{idx}_submitted"
    ans_key = f"q{idx}_user_answer"
    show_key = f"q{idx}_show_answer"
    
    cleaned_check = st.session_state[ans_key].strip()
    if st.session_state[sub_key] and cleaned_check == item["a"]:
        correct_count += 1

st.write(f"Total Correct Answers: {correct_count} / 10 required")

for idx, item in enumerate(questions_data, start=1):
    sub_key = f"q{idx}_submitted"
    ans_key = f"q{idx}_user_answer"
    show_key = f"q{idx}_show_answer"

    st.subheader(f"Question {idx}")
    st.write(item["q"])

    with st.form(key=f"quiz_form_q{idx}"):
        user_input = st.text_input("Your Answer:", value=st.session_state[ans_key], key=f"input_q{idx}")
        submit_button = st.form_submit_button(label="Submit Answer")

        if submit_button:
            st.session_state[sub_key] = True
            st.session_state[ans_key] = user_input

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Show Answer", key=f"btn_show_{idx}"):
            st.session_state[show_key] = not st.session_state[show_key]

    if st.session_state[show_key]:
        st.info(f"The correct answer is: {item['a']}")

    if st.session_state[sub_key]:
        cleaned_answer = st.session_state[ans_key].strip()
        if cleaned_answer == item["a"]:
            st.success("Correct! Well done.")
        elif cleaned_answer == "":
            st.warning("Please enter an answer before submitting.")
        else:
            st.error(f"Incorrect. You answered '{cleaned_answer}', but the correct answer is {item['a']}.")
    
    st.write("---")

if correct_count >= 10:
    st.balloons()
    st.header("End Game Unlocked!")
    
    if "clicks" not in st.session_state:
        st.session_state.clicks = 0
        
    st.write(f"Score: {st.session_state.clicks}")
    if st.button("CLICK ME FAST", key="game_clicker_button"):
        st.session_state.clicks += 1
        st.rerun()

has_any_submission = any(st.session_state[f"q{idx}_submitted"] for idx in range(1, len(questions_data) + 1))
if has_any_submission and st.button("Reset Quiz Entirely"):
    for idx in range(1, len(questions_data) + 1):
        st.session_state[f"q{idx}_submitted"] = False
        st.session_state[f"q{idx}_user_answer"] = ""
        st.session_state[f"q{idx}_show_answer"] = False
    if "clicks" in st.session_state:
        st.session_state.clicks = 0
    st.rerun()
