#!/usr/bin/env python3
"""
E-Tongue GUI (6 Tastes) — With Horizontal Bar Graph + Dominant LED
Tastes: Pungent, Sweet, Sour, Astringent, Bitter, Salt
LED Pins:
  Pungent -> 17
  Sweet   -> 27
  Sour    -> 22
  Astringent -> 5
  Bitter  -> 6
  Salt    -> 13
"""

import tkinter as tk
from tkinter import Toplevel, messagebox
import threading
import time

# -------------------------
# GPIO SETUP
# -------------------------
try:
    import RPi.GPIO as GPIO
    ON_PI = True
except:
    ON_PI = False
    class MockGPIO:
        BCM='BCM'; OUT='OUT'; HIGH=1; LOW=0
        def setmode(self, x): print("[GPIO-MOCK] setmode", x)
        def setup(self, p, m): print(f"[GPIO-MOCK] setup {p}")
        def output(self, p, v): print(f"[GPIO-MOCK] write {p} -> {v}")
        def cleanup(self): print("[GPIO-MOCK] cleanup")
    GPIO = MockGPIO()

GPIO.setmode(GPIO.BCM)

LED_PINS = {
    "Pungent": 17,
    "Sweet": 27,
    "Sour": 22,
    "Astringent": 5,
    "Bitter": 6,
    "Salt": 13
}

for p in LED_PINS.values():
    try:
        GPIO.setup(p, GPIO.OUT)
        GPIO.output(p, GPIO.LOW)
    except:
        pass

# -------------------------
# FUZZY FUNCTIONS
# -------------------------
def fuzzy(v, low, mid, high):
    try: v=float(v)
    except: return 0
    if v<=low or v>=high: return 0
    if v==mid: return 1
    if v<mid:
        return (v-low)/(mid-low)
    return (high-v)/(high-mid)

def taste_scores(pH, cond, tds, ir, dielectric):
    s = {t:0.0 for t in ["Pungent","Sweet","Sour","Astringent","Bitter","Salt"]}

    # pH
    s["Sour"] += fuzzy(pH, 2.5,3.5,4.5)
    s["Astringent"] += fuzzy(pH, 4,5,6)
    s["Sweet"] += fuzzy(pH, 5.5,6.2,7)
    s["Pungent"] += fuzzy(pH, 5,6,7.5)
    s["Bitter"] += fuzzy(pH, 4.5,6,9)
    s["Salt"] += fuzzy(pH, 6.5,7.5,9)

    # Conductivity
    s["Sweet"] += fuzzy(cond,0.1,0.3,0.5)
    s["Pungent"] += fuzzy(cond,0.2,0.6,1.0)
    s["Bitter"] += fuzzy(cond,0.3,1,2)
    s["Astringent"] += fuzzy(cond,0.4,1.4,2.5)
    s["Sour"] += fuzzy(cond,0.4,1.4,2.5)
    s["Salt"] += fuzzy(cond,1.5,2.5,3)

    # TDS
    s["Sweet"] += fuzzy(tds,100,250,400)
    s["Pungent"] += fuzzy(tds,150,350,600)
    s["Bitter"] += fuzzy(tds,200,500,900)
    s["Astringent"] += fuzzy(tds,300,750,1200)
    s["Sour"] += fuzzy(tds,300,750,1200)
    s["Salt"] += fuzzy(tds,500,1000,1500)

    # IR
    s["Bitter"] += fuzzy(ir,0.5,1,1.5)
    s["Astringent"] += fuzzy(ir,1.5,2.5,3.5)
    s["Sour"] += fuzzy(ir,1.5,2.5,3.5)
    s["Pungent"] += fuzzy(ir,2,3,3.8)
    s["Sweet"] += fuzzy(ir,3.5,4,4.5)
    s["Salt"] += fuzzy(ir,3.8,4.1,4.5)

    # Dielectric
    s["Salt"] += fuzzy(dielectric,40,55,70)
    s["Sour"] += fuzzy(dielectric,35,50,65)
    s["Astringent"] += fuzzy(dielectric,25,40,55)
    s["Pungent"] += fuzzy(dielectric,20,35,50)
    s["Sweet"] += fuzzy(dielectric,10,20,30)
    s["Bitter"] += fuzzy(dielectric,5,15,25)

    return s

# -------------------------
# AGE ANALYSIS
# -------------------------
def analyze_age(pH, ir):
    try:
        pH=float(pH); ir=float(ir)
    except: return 0,"Unknown","Invalid","Invalid"

    if pH<=3: days=0; status="Very Fresh"; reason="Low pH"; just="High acidity = fresh"
    elif pH<=4: days=15; status="Fresh"; reason="pH rising"; just="Early changes"
    elif pH<=5.2: days=30; status="Moderate"; reason="pH drift"; just="Chemical transition"
    elif pH<=6.5: days=45; status="Aged"; reason="Near neutral pH"; just="Age increase"
    else: days=60; status="Old"; reason="Highly neutral pH"; just="Prolonged storage"

    if ir<2: days=min(60,days+5)
    if ir>4: days=max(0,days-5)

    return days,status,reason,just

# -------------------------
# LED CONTROL — ONLY DOMINANT
# -------------------------
def light_led(taste, duration=5):
    pin = LED_PINS.get(taste)
    if not pin:
        print("[ERROR] Taste not mapped to LED")
        return

    def worker():
        try: GPIO.output(pin, GPIO.HIGH)
        except: pass
        time.sleep(duration)
        try: GPIO.output(pin, GPIO.LOW)
        except: pass

    threading.Thread(target=worker,daemon=True).start()


# -------------------------
# OUTPUT WINDOW (WITH BAR GRAPH)
# -------------------------
def show_output_window(text_content, dominant_taste, percent_data):
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    win = Toplevel()
    win.title("E-Tongue Analysis Result")
    win.geometry("780x440+10+10")
    win.configure(bg="#F6F4EF")

    canvas = tk.Canvas(win, bg="#F6F4EF")
    vsb = tk.Scrollbar(win, orient="vertical", command=canvas.yview)
    frame = tk.Frame(canvas, bg="#F6F4EF", padx=12, pady=12)

    canvas.create_window((0, 0), window=frame, anchor="nw")
    canvas.configure(yscrollcommand=vsb.set)

    canvas.pack(side="left", fill="both", expand=True)
    vsb.pack(side="right", fill="y")

    # Text box
    txt = tk.Text(frame, wrap="word", font=("Arial", 13), bg="#F6F4EF", bd=0)
    txt.pack(fill="both", expand=True)
    txt.insert("1.0", text_content)

    txt.config(state="disabled")

    # --------------------
    # Horizontal Bar Graph
    # --------------------
    fig = Figure(figsize=(6.5, 3.5), dpi=100)
    ax = fig.add_subplot(111)

    tastes = list(percent_data.keys())
    values = list(percent_data.values())

    ax.barh(tastes, values)
    ax.set_xlabel("Strength (%)")
    ax.set_title("Taste Intensity Distribution")
    ax.grid(True, axis='x', linestyle='--', alpha=0.3)

    fig.tight_layout()

    graph_canvas = FigureCanvasTkAgg(fig, master=frame)
    graph_canvas.draw()
    graph_canvas.get_tk_widget().pack(pady=15)

    frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

    light_led(dominant_taste)


# -------------------------
# INPUT WINDOW
# -------------------------
def input_window(root):
    win=Toplevel(root)
    win.geometry("780x440+10+10")
    win.title("Enter Sensor Values")

    canvas=tk.Canvas(win)
    vs=tk.Scrollbar(win,command=canvas.yview)
    frame=tk.Frame(canvas,padx=15,pady=15)
    canvas.create_window((0,0),window=frame,anchor="nw")
    canvas.configure(yscrollcommand=vs.set)
    canvas.pack(side="left",fill="both",expand=True)
    vs.pack(side="right",fill="y")

    fields=[("pH","4.0"),("Conductivity","1.0"),("TDS","500"),("IR Voltage","2.0"),("Dielectric","40")]
    entries={}

    for lbl,defv in fields:
        tk.Label(frame,text=lbl,font=("Arial",14)).pack(anchor="w")
        e=tk.Entry(frame,font=("Arial",16))
        e.insert(0,defv)
        e.pack(fill="x",pady=5)
        entries[lbl]=e

    def run():
        try:
            pH=float(entries["pH"].get())
            cond=float(entries["Conductivity"].get())
            tds=float(entries["TDS"].get())
            ir=float(entries["IR Voltage"].get())
            diel=float(entries["Dielectric"].get())
        except:
            messagebox.showerror("Error","Invalid input")
            return

        raw = taste_scores(pH,cond,tds,ir,diel)
        total=sum(raw.values()) or 1e-9
        percent={k:(v/total)*100 for k,v in raw.items()}
        sorted_p = sorted(percent.items(), key=lambda x:x[1], reverse=True)

        dominant = sorted_p[0][0]

        days,status,reason,just = analyze_age(pH,ir)

        text = (
            f"✨ Strongest Taste Identified: '{dominant}' ✨\n\n"
            f"Dominant Taste: {dominant} ({sorted_p[0][1]:.2f}%)\n\n"
            "Taste Breakdown:\n" +
            "\n".join([f"{k}: {v:.2f}%" for k,v in sorted_p]) +
            "\n\n-----------------------------\n"
            f"AGE ESTIMATION: {days} days — {status}\n"
            f"Reason: {reason}\n"
            f"Justification: {just}\n"
        )

        show_output_window(text, dominant, percent)

    tk.Button(frame,text="Run Analysis",font=("Arial",18,"bold"),
              bg="#0A9441",fg="white",command=run).pack(pady=20)

    frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

# -------------------------
# MAIN
# -------------------------
def main():
    root = tk.Tk()
    root.geometry("800x480")
    root.title("PudhuValzhi E-Tongue")

    tk.Label(root, text="PudhuValzhi E-Tongue",
             font=("Arial",28,"bold")).pack(pady=20)

    tk.Button(root, text="Start Measurement", font=("Arial",20,"bold"),
              bg="#0A9441", fg="white", width=20,
              command=lambda: input_window(root)).pack(pady=30)

    root.mainloop()

if __name__ == "__main__":
    main()
