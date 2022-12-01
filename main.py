import streamlit as st
import plot

dac_ta = st.text_input("Nhập vào đặc tả:")
gia_tri_dien_tro = st.text_input("Nhập vào giá trị các điện trở:")

click = st.button("Biểu diễn")
if click:
    result = plot.main(dac_ta, gia_tri_dien_tro)
    st.image('picture.png', caption='Sơ đồ mạch điện')
    st.write('Tổng trở của mạch điện là: ', result)