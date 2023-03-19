from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import PIL
import torch
from PIL import Image
from torchvision import transforms
import urllib.request
import requests
from datetime import datetime
import os
from twilio.rest import Client
api_url = 'https://api.api-ninjas.com/v1/imagetotext'
api_phone = "https://api.api-ninjas.com/v1/validatephone?number="

app = Flask(__name__)
model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet50', pretrained=True)
model.eval()

api_key = "secret"

name = ""
phone_number = ""

account_sid = 'secret'
auth_token = 'secret'
client = Client(account_sid, auth_token)

@app.route('/',methods=['GET', 'POST'])
def index():
    global name
    global phone_number
    global api_phone
    if request.method == "POST":
        name = request.form["name"]
        phone_number = request.form["phonenumber"]
        api_phone ="https://api.api-ninjas.com/v1/validatephone?number=" + phone_number
        response = requests.get(api_phone, headers={'X-Api-Key': api_key})
        response = response.text
        print(type(response))
        error_message = {"error": "number parameter must be provided."}
        # if response.json()[is_valid] == True:
        if response.find("true") != -1:
            print(response)
            return redirect(url_for('upload'))
        else:
            print(api_phone)
            print(phone_number)
    return render_template('index.html')

medication_names = ["ACICLOVIR (ZOVIRAX)", "ACRIVASTINE", "ADALIMUMAB", "ALENDRONIC ACID", "ALLOPURINOL", "ALOGLIPTIN", "AMITRIPTYLINE FOR DEPRESSION", "AMITRIPTYLINE FOR PAIN AND MIGRAINE", "AMLODIPINE", "AMOXICILLIN", "ANASTROZOLE", "APIXABAN", "ASPIRIN FOR PAIN RELIEF", "ASPIRIN – LOW-DOSE, SEE LOW-DOSE ASPIRIN", "ATENOLOL", "ATORVASTATIN", "AZATHIOPRINE", "AZITHROMYCIN", "BACLOFEN", "BECLOMETASONE INHALERS", "BECLOMETASONE NASAL SPRAY", "BECLOMETASONE SKIN CREAMS", "BECLOMETASONE TABLETS", "BENDROFLUMETHIAZIDE", "BENZOYL PEROXIDE", "BENZYDAMINE", "BETAHISTINE", "BETAMETHASONE FOR EYES, EARS AND NOSE", "BETAMETHASONE FOR SKIN", "BETAMETHASONE TABLETS", "BIMATOPROST", "BISACODYL", "BISOPROLOL", "BRINZOLAMIDE", "BUDESONIDE INHALERS", "BUDESONIDE NASAL SPRAY", "BUDESONIDE RECTAL FOAM AND ENEMAS", "BUDESONIDE TABLETS, CAPSULES AND GRANULES", "BUMETANIDE", "BUPRENORPHINE FOR PAIN", "BUSCOPAN (HYOSCINE BUTYLBROMIDE)", "CALCIPOTRIOL", "CANDESARTAN", "CARBAMAZEPINE", "CARBIMAZOLE", "CARBOCISTEINE", "CARMELLOSE SODIUM", "CARVEDILOL", "CEFALEXIN", "CETIRIZINE", "CHAMPIX (VARENICLINE)", "CHLORAMPHENICOL", "CHLORHEXIDINE", "CHLORPHENAMINE (PIRITON)", "CINNARIZINE", "CIPROFLOXACIN", "CITALOPRAM", "CLARITHROMYCIN", "CLOBETASOL", "CLOBETASONE", "CLONAZEPAM", "CLONIDINE", "CLOPIDOGREL", "CLOTRIMAZOLE CREAM, SPRAY AND SOLUTION", "CLOTRIMAZOLE FOR THRUSH (CANESTEN)", "CO-AMOXICLAV", "CO-BENELDOPA", "CO-CARELDOPA", "CO-CODAMOL FOR ADULTS", "CO-CODAMOL FOR CHILDREN", "CO-CODAPRIN (ASPIRIN AND CODEINE)", "CO-DYDRAMOL", "COAL TAR", "CODEINE", "COLCHICINE", "COLECALCIFEROL", "CYANOCOBALAMIN", "CYCLIZINE", "DABIGATRAN", "DAPAGLIFLOZIN", "DEXAMETHASONE EYE DROPS", "DEXAMETHASONE TABLETS AND LIQUID", "DIAZEPAM", "DICLOFENAC", "DIGOXIN", "DIHYDROCODEINE", "DILTIAZEM", "DIPHENHYDRAMINE", "DIPYRIDAMOLE", "DOCUSATE", "DOMPERIDONE", "DONEPEZIL", "DOSULEPIN", "DOXAZOSIN", "DOXYCYCLINE", "DULOXETINE", "EDOXABAN", "EMPAGLIFLOZIN", "ENALAPRIL", "EPLERENONE", "ERYTHROMYCIN", "ESCITALOPRAM", "ESOMEPRAZOLE", "EZETIMIBE", "FELODIPINE", "FENTANYL", "FERROUS FUMARATE", "FERROUS SULFATE", "FEXOFENADINE", "FINASTERIDE", "FLUCLOXACILLIN", "FLUCONAZOLE", "FLUOXETINE (PROZAC)", "FLUTICASONE INHALERS", "FLUTICASONE NASAL SPRAY AND DROPS", "FLUTICASONE SKIN CREAMS", "FOLIC ACID", "FUROSEMIDE", "FUSIDIC ACID", "FYBOGEL (ISPAGHULA HUSK)", "GABAPENTIN", "GAVISCON (ALGINIC ACID)", "GLICLAZIDE", "GLIMEPIRIDE", "GLYCERYL TRINITRATE (GTN)", "HEPARINOID", "HYDROCORTISONE", "HYDROCORTISONE BUCCAL TABLETS", "HYDROCORTISONE FOR PILES AND ITCHY BOTTOM", "HYDROCORTISONE FOR SKIN", "HYDROCORTISONE INJECTIONS", "HYDROCORTISONE RECTAL FOAM", "HYDROCORTISONE TABLETS", "HYDROXOCOBALAMIN", "HYDROXYCHLOROQUINE", "HYOSCINE HYDROBROMIDE (KWELLS AND JOY-RIDES)", "IBUPROFEN AND CODEINE", "IBUPROFEN FOR ADULTS (NUROFEN)", "IBUPROFEN FOR CHILDREN", "INDAPAMIDE", "IRBESARTAN", "ISOSORBIDE MONONITRATE AND ISOSORBIDE DINITRATE", "ISOTRETINOIN CAPSULES (ROACCUTANE)", "ISOTRETINOIN GEL (ISOTREX)", "INOPRIL","KETOCONAZOLE", "LABETALOL", "LACTULOSE", "LAMOTRIGINE", "LANSOPRAZOLE", "LATANOPROST", "LERCANIDIPINE", "LETROZOLE", "LEVETIRACETAM", "LEVOTHYROXINE", "LIDOCAINE FOR MOUTH AND THROAT", "LIDOCAINE FOR PILES AND ITCHY BOTTOM", "LIDOCAINE SKIN CREAM", "LINAGLIPTIN", "LISINOPRIL", "LITHIUM", "LOPERAMIDE", "LORATADINE (CLARITYN)", "LORAZEPAM", "LOSARTAN", "LOW-DOSE ASPIRIN", "LYMECYCLINE", "BACK TO TOP", "M", "MACROGOL", "MEBENDAZOLE", "MEBEVERINE", "MELATONIN", "MEMANTINE", "MESALAZINE", "METFORMIN", "METHADONE", "METHOTREXATE", "METHYLPHENIDATE FOR ADULTS", "METHYLPHENIDATE FOR CHILDREN", "METOCLOPRAMIDE", "METOPROLOL", "METRONIDAZOLE", "MIRABEGRON", "MIRTAZAPINE", "MOLNUPIRAVIR (LAGEVRIO)", "MOMETASONE FOR SKIN", "MOMETASONE INHALERS", "MOMETASONE NASAL SPRAY", "MONTELUKAST", "MORPHINE", "BACK TO TOP", "N", "NAPROXEN", "NEFOPAM", "NICORANDIL", "NIFEDIPINE", "NITROFURANTOIN", "NORTRIPTYLINE", "NYSTATIN", "BACK TO TOP", "O", "OLANZAPINE", "OLMESARTAN", "OMEPRAZOLE", "OXYBUTYNIN", "OXYCODONE", "BACK TO TOP", "P", "PANTOPRAZOLE", "PARACETAMOL FOR ADULTS", "PARACETAMOL FOR CHILDREN (CALPOL)", "PAROXETINE", "PAXLOVID", "PEPPERMINT OIL", "PEPTO-BISMOL (BISMUTH SUBSALICYLATE)", "PERINDOPRIL", "PHENOXYMETHYLPENICILLIN", "PHENYTOIN", "PIOGLITAZONE", "PRAVASTATIN", "PRE-EXPOSURE PROPHYLAXIS (PREP)", "PREDNISOLONE TABLETS AND LIQUID", "PREGABALIN", "PROCHLORPERAZINE", "PROMETHAZINE (PHENERGAN)", "PROPRANOLOL", "BACK TO TOP", "Q", "QUETIAPINE", "BACK TO TOP", "R", "RABEPRAZOLE", "RAMIPRIL", "RANITIDINE", "REMDESIVIR (VEKLURY)", "RISEDRONATE", "RISPERIDONE", "RIVAROXABAN", "ROPINIROLE", "ROSUVASTATIN", "BACK TO TOP", "S", "SALBUTAMOL INHALER", "SAXAGLIPTIN", "SENNA", "SERTRALINE", "SILDENAFIL (VIAGRA)", "SIMETICONE", "SIMVASTATIN", "SITAGLIPTIN", "SODIUM CROMOGLICATE CAPSULES", "SODIUM CROMOGLICATE EYE DROPS", "SODIUM VALPROATE", "SOLIFENACIN", "SOTALOL", "SOTROVIMAB (XEVUDY)", "SPIRONOLACTONE", "SULFASALAZINE", "SUMATRIPTAN", "TADALAFIL", "TAMSULOSIN", "TEMAZEPAM", "TERBINAFINE", "THIAMINE (VITAMIN B1)", "TICAGRELOR", "TIMOLOL EYE DROPS", "TIMOLOL TABLETS", "TOLTERODINE", "TOPIRAMATE", "TRAMADOL", "TRANEXAMIC ACID", "TRAZODONE", "TRIMETHOPRIM", "VALPROIC ACID", "VALSARTAN", "VARENICLINE, SEE CHAMPIX (VARENICLINE)", "VENLAFAXINE", "VERAPAMIL", "WARFARIN", "ZOLPIDEM", "ZOPICLONE"]
medicine_name = "medicine name"
pill_count = "pill count"
frequency = "frequency"
form = "form"
med = []
isPill = False
image = ""
dictionary = {"medicine_name" : medicine_name, "pill_count" : pill_count, "frequency" : frequency, "form" : form, "time" : ""}
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    global isPill 
    if request.method == 'POST':
        file = request.files['image'].read()
        open('imag.jpg', 'wb').write(file)
        # if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        #     return redirect(url_for('upload'))
        # if not file.verify():
        #     return redirect(url_for('upload'))

        input_image = Image.open('imag.jpg').convert('RGB')
        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        input_tensor = preprocess(input_image)
        input_batch = input_tensor.unsqueeze(0) 
        if torch.cuda.is_available():
            input_batch = input_batch.to('cuda')
            model.to('cuda')
        with torch.no_grad():
            output = model(input_batch)
        #print(output[0])
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        #print(probabilities)
        urllib.request.urlretrieve("https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt", filename="imagenet_classes.txt")
        # Read the categories
        with open("imagenet_classes.txt", "r") as f:
            categories = [s.strip() for s in f.readlines()]
        # Show top categories per image
        top5_prob, top5_catid = torch.topk(probabilities, 5)
        print("success")
        #for i in range(top5_prob.size(0)):
            #print(categories[top5_catid[i]], top5_prob[i].item())
        if categories[top5_catid[0]] == "pill bottle":
            #scan scan scan and add variable to results
            image_file_descriptor = open('imag.jpg', 'rb')
            print("1")
            files = {'image': image_file_descriptor}
            print("2")                  
            r = requests.post(api_url, files=files, headers={'X-Api-Key': api_key})
            r = r.json()
            pill_count_keywords = ["one", "two", "three", "four", "five", "six"]
            frequency_keywords = ["once", "twice", "thrice", "four times", "three times", "two times",]
            form_keywords = ["liquid", "tablet", "tablets", "foam", "gummy", "serum", "drop", "syrup"]
            for i in r:
                if i['text'].upper() in medication_names:
                    global medicine_name
                    medicine_name = i['text'].capitalize()       

                if i['text'].lower() in pill_count_keywords:
                    global pill_count
                    pill_count = i['text'].lower()
                if i['text'].lower() in frequency_keywords:
                    global frequency
                    frequency = i['text'].lower()
                if i['text'].lower() in form_keywords:
                    global form
                    form = i['text'].lower()
            global med
            global dictionary
            dictionary = {"medicine_name" : medicine_name, "pill_count" : pill_count, "frequency" : frequency, "form" : form}
            isPill = True
            return redirect(url_for('results'))
            
        else:
            global image
            image = categories[top5_catid[0]]
            print("not pill bottle is", image)
            # return redirect(url_for('upload'))
            isPill = False
            return redirect(url_for('results'))

    return render_template('upload.html')

@app.route('/results',methods=['GET','POST'])
def results():
    global med
    global dictionary
    global name
    # if request.method == 'POST':
    if "right" in request.form:
        time = request.form["time"]
        dictionary["time"] = time
        if dictionary not in med:
            med.append(dictionary)
            hour = int(time[0:2]) + 7
            minute = int(time[3:5])
            print(hour, minute)
            # message = client.messages \
            #     .create(
            #         messaging_service_sid='MG2f0d9d258f843aa1a9917baa4397abb4',
            #         from_='+18885217558',
            #         body='This is a reminder to take ' + dictionary["pill_count"]+ dictionary["form"] + " of " +dictionary["medicine_name"] + " now :)",
            #         send_at=datetime(2023, 3, 19, hour, minute, 0),
            #         schedule_type='fixed',
            #         status_callback='https://webhook.site/xxxxx',
            #         to=phone_number
            #     )
            # print(message.sid)
            print(time)
        return redirect(url_for('list'))
    elif "wrong" in request.form:
        return redirect(url_for('upload'))
    elif "uploadagain" in request.form:
        return redirect(url_for('upload'))
    print(medicine_name, frequency, pill_count, form, image)
    return render_template('results.html', isPill = isPill, medicine = medicine_name, frequency = frequency, count = pill_count, form = form, full = med, image = image)

@app.route('/list',methods=['GET','POST'])
def list():
    global med
    if "uploadagain" in request.form:
        return redirect(url_for('upload'))
    return render_template('list.html', med = med, name = name)