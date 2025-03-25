import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch.nn.functional as F

# Define Paths
model_path = "./saved_model"  # Update this if your model is saved elsewhere

# Load Tokenizer and Model
tokenizer = DistilBertTokenizer.from_pretrained(model_path)
model = DistilBertForSequenceClassification.from_pretrained(model_path)

# Department List (21 labels)
DEPARTMENT_LIST = [
    "Revenue Department", "Social Welfare Department", "Rural Development",
    "Urban Development", "Engineering Department (PWD, Electricity Board, Water Board)",
    "Agriculture-related Departments", "Education Department", "Health Departments",
    "Police Department", "Cooperative Department", "Registration Department",
    "Public Welfare (Ex-Army / Military Welfare)", "Pension Directorate",
    "Hindu Religious and Charitable Endowments", "Tamil Nadu Housing Board",
    "Judiciary", "Welfare of Differently Abled Persons",
    "Tamil Nadu Slum Clearance Board", "Survey and Settlement Department",
    "Handloom and Textiles Department", "Land Administration Department"
]

# Verify Department List Length
print(f"✅ Department List (Length: {len(DEPARTMENT_LIST)}): {DEPARTMENT_LIST}")
print(f"✅ Model output labels: {model.config.num_labels}")

# Define Inference Function
def get_department(petition_details):
    try:
        # Tokenize the input text
        inputs = tokenizer(petition_details, return_tensors="pt", truncation=True, max_length=512)
        
        # Set model to evaluation mode
        model.eval()
        
        # Disable gradient calculation for inference
        with torch.no_grad():
            outputs = model(**inputs)
        
        # Get raw logits
        logits = outputs.logits
        
        # Apply softmax to get probabilities
        probabilities = F.softmax(logits, dim=1)[0]  # Get first element
        
        # Get the highest probability and corresponding department
        top_prob, top_class = torch.max(probabilities, dim=0)
        
        # Get predicted department
        predicted_department = DEPARTMENT_LIST[top_class.item()]
        
        # Debug: Print Raw Output
        print(f"\n🟢 Full model output: {probabilities.tolist()}")
        print(f"✅ Top label: {predicted_department}, Score: {top_prob.item():.4f}")
        
        return predicted_department
    
    except Exception as e:
        print(f"❌ Error in get_department(): {e}")
        return "Unknown Department"

# Test the function
input_text = "Applying for pension"
print(f"Input Text: {input_text}")
predicted_department = get_department(input_text)
print(f"🎯 Predicted Department: {predicted_department}")
