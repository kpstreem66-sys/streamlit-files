import streamlit as st

st.title("The Worthiness Test Workspace")
st.write("Hello World! Let's test if you are worthy of this project.")

# Initialize score in the web browser's memory
if "worthiness" not in st.session_state:
    st.session_state.worthiness = 0

# Question 1
q1 = st.text_input("What is 2x8?", key="q1")
if q1:
    if q1 == "16":
        st.success("Correct! Worthiness level = 5%")
        st.session_state.worthiness = 5
        
        # Question 2 (Only shows if Question 1 is correct)
        q2 = st.text_input("What is 64/8x(3+1)2?", key="q2")
        if q2:
            if q2 == "128":
                st.success("Correct! Worthiness level = 15%")
                st.session_state.worthiness = 15
                
                # Question 3
                q3 = st.text_input("What is 2x8x(5)2+(3+4)2?", key="q3")
                if q3:
                    if q3 == "449":
                        st.success("Correct! Worthiness level = 100%")
                        st.balloons() # Celebratory animation in browser!
                        st.write("### Access Granted! You are worthy of this workspace.")
                    else:
                        st.error("Incorrect. Access Denied.")
            else:
                st.error("Incorrect. Access Denied.")
    else:
        st.error("Incorrect. Access Denied.")
