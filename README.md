# Pudhuvalzhi’s e-Tongue  
Fuzzy Logic-Based Multi-Sensor Electronic Taste Prediction System  

🏆 Developed for Smart India Hackathon 2025  

---

## Overview

Pudhuvalzhi’s e-Tongue is an intelligent embedded system designed to predict the taste profile of Ayurvedic liquid samples using multi-sensor fusion and fuzzy logic.

The system integrates chemical, electrical, optical, and electromagnetic sensing mechanisms and processes the extracted features through a Fuzzy Inference System (FIS) to classify taste and estimate percentage composition.

The complete system is implemented using Raspberry Pi with a touchscreen interface for real-time display of results.

---

## Problem Statement

Traditional taste evaluation of Ayurvedic liquids relies on subjective human sensory perception, which may vary between individuals.

There is a need for a standardized, reproducible, and technology-driven method to analyze and quantify taste attributes.

---

## Objectives

• Measure physicochemical and electromagnetic properties of liquid samples  
• Extract meaningful multi-sensor features  
• Implement fuzzy logic-based decision system  
• Predict primary taste category  
• Estimate percentage composition of taste attributes  

---

## System Workflow

Sample Preparation → Multi-Sensor Data Acquisition → Feature Extraction → Normalization → Fuzzy Inference Engine → Taste Prediction → Percentage Output

---

## Sample Preparation Protocol

1. Weigh 1 g of Ayurvedic sample  
2. Add 40 mL of distilled water  
3. Label and prepare for sensor measurement  

---

## Sensor Architecture

The system integrates six sensing mechanisms:

### 1. pH Measurement
- Measures acidity/alkalinity  
- Low pH → Sour profile  

### 2. TDS Measurement
- Measures dissolved solids  
- High TDS → Mineral/Salty characteristics  

### 3. Conductivity Measurement
- Indicates ionic strength  
- Differentiates ionic and non-ionic compounds  

### 4. IR Absorption Voltage
- Bitter compounds → Higher absorption (Low voltage)  
- Sweet compounds → Higher transmission (High voltage)  

### 5. Permittivity (Capacitance-Based)
- Determines dielectric properties  
- Polar molecules increase permittivity  

### 6. CSRR-Based S-Parameter Analysis
- Detects electromagnetic resonance shifts  
- Enables high-sensitivity structural identification  

---

## Feature Extraction

Recorded parameters:

- pH  
- TDS  
- Conductivity  
- IR Voltage  
- Permittivity  
- CSRR S-parameters  

All features are normalized before processing.

---

## Intelligent Decision System

The system uses a Fuzzy Logic-based Inference Engine.

Steps involved:

1. Convert sensor values into fuzzy membership functions (Low / Medium / High)
2. Apply rule-based IF–THEN inference
3. Perform defuzzification to compute crisp output

Example Rule:

IF pH is Low AND Conductivity is Medium  
THEN Taste is Sour (High Confidence)

---

## Hardware Implementation

• Raspberry Pi  
• Multi-sensor integration modules  
• Touchscreen display interface  
• Embedded data acquisition system  

The touchscreen displays:

✔ Primary predicted taste  
✔ Percentage composition of taste attributes  

---

## Output

• Primary taste category  
• Percentage distribution of taste attributes  
• Sensor-based interpretation  

Example Interpretation:

- Low pH → High Sourness  
- High TDS & Conductivity → Salty profile  
- Low IR Voltage → Bitter compounds  
- High Permittivity → Ionic dominance  
- CSRR Resonance Shift → Complex molecular structure  

---

## Impact

✔ Reduces subjectivity in taste evaluation  
✔ Provides standardized testing method  
✔ Integrates AI with embedded hardware  
✔ Suitable for Ayurvedic formulation analysis  

---

## Future Enhancements

• Expansion of dataset  
• Integration with cloud-based analytics  
• IoT-based remote monitoring  
• Deep learning comparison models  

---

📌 Smart India Hackathon 2025 Project  
📌 Implemented using Raspberry Pi and Fuzzy Inference System
