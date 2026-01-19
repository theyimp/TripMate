import streamlit as st
import pandas as pd
import random

# 1. ตั้งค่าหน้าเว็บให้เหมาะกับมือถือ
st.set_page_config(
    page_title="TripMate",
    page_icon="✈️",
    layout="centered", # ใช้ centered จะอ่านง่ายกว่าบนมือถือ
    initial_sidebar_state="collapsed" # ซ่อนเมนูข้างเพื่อไม่ให้เกะกะ
)

# --- CSS ปรับแต่งพิเศษสำหรับ Mobile ---
st.markdown("""
<style>
    .stButton button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        font-weight: bold;
    }
    .place-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        border-left: 5px solid #ff4b4b;
    }
    h1, h2, h3 {
        font-family: 'Sarabun', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. ฐานข้อมูลสถานที่ (Mock Data) ---
# ในอนาคตสามารถเปลี่ยนตรงนี้เป็นดึงจาก Google Sheets หรือ CSV ได้
db_places = {
    "เชียงใหม่": [
        {"name": "วัดพระสิงห์", "type": "Culture", "lat": 18.788, "lon": 98.982},
        {"name": "ถนนนิมมานเหมินท์", "type": "Cafe", "lat": 18.799, "lon": 98.968},
        {"name": "ดอยสุเทพ", "type": "Nature", "lat": 18.804, "lon": 98.921},
        {"name": "ร้านข้าวซอยแม่สาย", "type": "Food", "lat": 18.801, "lon": 98.965},
        {"name": "ม่อนแจ่ม", "type": "Nature", "lat": 18.935, "lon": 98.822},
        {"name": "ตลาดวโรรส (กาดหลวง)", "type": "Food", "lat": 18.790, "lon": 99.000},
    ],
    "ภูเก็ต": [
        {"name": "แหลมพรหมเทพ", "type": "Nature", "lat": 7.763, "lon": 98.305},
        {"name": "ย่านเมืองเก่าภูเก็ต", "type": "Culture", "lat": 7.886, "lon": 98.390},
        {"name": "หาดป่าตอง", "type": "Nature", "lat": 7.896, "lon": 98.295},
        {"name": "ร้านตู้กับข้าว", "type": "Food", "lat": 7.883, "lon": 98.391},
    ]
}

# --- 3. ส่วนแสดงผล (User Interface) ---
st.title("TripMate ✈️")
st.caption("ผู้ช่วยจัดทริปบนมือถือของคุณ")

# ส่วนรับข้อมูล (Input)
with st.expander("📝 ตั้งค่าการเดินทาง", expanded=True):
    destination = st.selectbox("ไปเที่ยวที่ไหน?", list(db_places.keys()))
    days = st.slider("จำนวนวัน", 1, 5, 2)
    interests = st.multiselect(
        "สไตล์ที่ชอบ",
        ["Nature", "Culture", "Cafe", "Food"],
        default=["Nature", "Food"]
    )
    
    if st.button("🚀 จัดทริปเลย!", type="primary"):
        st.session_state['generated'] = True
        st.session_state['dest'] = destination
        st.session_state['days'] = days
        st.session_state['interests'] = interests

# --- 4. Logic จัดทริปและแสดงผล ---
if 'generated' in st.session_state and st.session_state['generated']:
    
    selected_dest = st.session_state['dest']
    places = db_places[selected_dest]
    
    # กรองสถานที่ตามความสนใจ
    user_interests = st.session_state['interests']
    filtered_places = [p for p in places if p['type'] in user_interests or p['type'] == 'Food']
    
    # ถ้าไม่มีสถานที่ตรงใจเลย ให้เอามาทั้งหมด
    if not filtered_places:
        filtered_places = places

    st.divider()
    st.subheader(f"🗺️ แผนเที่ยว: {selected_dest}")
    
    # วนลูปสร้างตารางเที่ยวตามจำนวนวัน
    random.shuffle(filtered_places) # สุ่มลำดับ (ในอนาคตใช้ Logic ระยะทาง)
    
    place_index = 0
    for day in range(1, st.session_state['days'] + 1):
        st.markdown(f"#### 🗓️ Day {day}")
        
        # จัด 3 สถานที่ต่อวัน (เช้า/บ่าย/เย็น)
        activities = ["ช่วงเช้า", "ช่วงบ่าย (หาของกิน)", "ช่วงเย็น"]
        
        for time_slot in activities:
            if place_index < len(filtered_places):
                place = filtered_places[place_index]
                
                # สร้าง Card สถานที่
                google_maps_url = f"https://www.google.com/maps/search/?api=1&query={place['name']}+{selected_dest}"
                
                st.markdown(f"""
                <div class="place-card">
                    <b>{time_slot}</b><br>
                    <span style="font-size:1.2em;">📍 {place['name']}</span><br>
                    <span style="color:gray; font-size:0.8em;">{place['type']}</span>
                </div>
                """, unsafe_allow_html=True)
                
                # ปุ่มกดไป Google Maps
                st.link_button(f"🚗 นำทางไป {place['name']}", google_maps_url)
                
                place_index += 1
            else:
                st.info("พักผ่อนตามอัธยาศัย")
                break
        
        st.markdown("---")

