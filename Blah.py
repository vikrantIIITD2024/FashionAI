import pandas as pd
import json
# import os
import sys
import numpy as np

from nltk.tokenize import word_tokenize#, sent_tokenize
import nltk

def update_nltk():
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('state_union')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')


from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import stopwords
import re

def loadData():
    df_acc = pd.read_excel("../../META DATASET/xlsx/Accessories.xlsx")
    df_dress = pd.read_excel("../../META DATASET/xlsx/outfits.xlsx")
    df_foot = pd.read_excel("../../META DATASET/xlsx/footwears.xlsx")
    return (df_acc, df_dress, df_foot)



def extract_gender(text):
    male_terms = set([
        "male", "man", "boy", "men", "guy", "gentleman", "sir", "he", "his",
        "him", "mr", "father", "dad", "son", "brother", "uncle", "grandfather",
        "nephew", "husband", "boyfriend", "king", "prince", "king", "sir", "mr"
    ])

    female_terms = set([
        "female", "woman", "girl", "women", "lady", "she", "her", "hers", "mrs",
        "miss", "ms", "mother", "mom", "daughter", "sister", "aunt", "grandmother",
        "niece", "wife", "girlfriend", "queen", "princess", "madam", "ma'am", "misses"
    ])

    # Tokenize the input text
    tokens = word_tokenize(text.lower())

    # Check if any male term is present
    if any(term in tokens for term in male_terms):
        return "M"
    # Check if any female term is present
    elif any(term in tokens for term in female_terms):
        return "F"
    else:
        return "Unknown"

def main(sample_text):
  # Define lists for regions, age groups, and occasions
  city_states = locations()
  regions_in_india = ["delhi", "maharashtra", "chennai","south-india","kolkata", "bangalore", "hyderabad", "jaipur", "lucknow", "chandigarh"]
  clothExtract = {
    'shoes': 'footwear',
    'boots': 'footwear',
    'sneakers': 'footwear',
    'sandals': 'footwear',
    'flip-flops': 'footwear',
    'slippers': 'footwear',
    'heels': 'footwear',
    'flats': 'footwear',
    'loafers': 'footwear',
    'footwear': 'footwear',
    'dress':'dress',
    'gown': 'dress',
    'frock': 'dress',
    'attire': 'dress',
    'outfit': 'dress',
    'garment': 'dress',
    'apparel': 'dress',
    'ensemble': 'dress',
    'robe': 'dress',
    'clothing': 'dress',
    'suit': 'dress',
    'jewelry': 'accessories',
    'handbag': 'accessories',
    'purse': 'accessories',
    'wallet': 'accessories',
    'belt': 'accessories',
    'scarf': 'accessories',
    'hat': 'accessories',
    'glasses': 'accessories',
    'sunglasses': 'accessories',
    'watch': 'accessories',
    'accessories':'accessories'}
  # clothType = ["footwear", "dress", "accessories"]
  age_groups = {
      "teenager": (13, 17),
      "young adult": (18, 25),
      "pre-adult": (25, 35),
      "adult": (35, 45),
      "elder": (45, 55),
      "old": (55, 65)
  }

  categories = ["ethnics", "sarees", "kurtas", "casuals", "one-piece", "suit",
                "lehenga-choli", "gym", "anklet", "bracelet", "neckless",
                "jewellery", "watches", "sunglasses", "work", "sports",
                "formals", "boots", "sneakers", "winter", "heels"]



  occasions = ["durgapooja", "diwali", "groom", "wedding", "onam", "eid", "party",
               "pongal", "interview", "farewell", "sports",
               "walking", "running", "college", "lohri",
               "work", "karva-chauth", "office", "meeting", "conference",]

  # Sample text
  # sample_text = "A boy looking for college outfit in Delhi Region"


  bodyType = ["ectomorph", "mesomorph" ,"endomorph"]

  if ("durga pooja" in sample_text.lower()):
    newsample = ""
    words = sample_text.lower().split()
    for i in range(len(words)):
      try:
        if (words[i] == 'durga' and words[i+1] == 'pooja'):
          newsample += words[i]+words[i+1] + " "
        elif (words[i] == 'pooja' and words[i-1] == 'durga'):
          continue
        else:
          newsample += words[i] + " "
      except Exception as _:
                pass
    sample_text = newsample
  # Tokenize the text
  tokens = word_tokenize(sample_text.lower())

  # Remove stopwords
  stop_words = set(stopwords.words('english'))
  filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
  # print("filtered tokens: ", filtered_tokens)

  # Part-of-speech tagging
  tagged_words = pos_tag(filtered_tokens)
  # print("tagged words: ",tagged_words)

  # Initialize variables
  region = "any"
  age_group = (18,25)
  occasion = "any"
  gender = None
  bodyType = "Mesomorph"
  cat = "any"
  sheet = "dress"

  # Extract information based on part-of-speech tags
  for word, tag in tagged_words:
      if word in clothExtract.keys():
        sheet = clothExtract[word]
      if (word in city_states.keys() and city_states[word] in regions_in_india):
          region = city_states[word]
      if word in regions_in_india:
          region = word
      elif word in occasions:
          occasion = word
      elif word in bodyType:
          bodyType = word
      if word in categories:
        cat = word

  gender = extract_gender(sample_text)
  # print("Got gender", gender)



  # Check for specific phrases and map them to age groups
  # age group check flaw
  if "young" in sample_text:
      age_group = age_groups["young adult"]
  elif "young-old" in sample_text:
      age_group = age_groups["pre-adult"]
  else:
    # Convert the list of keywords to a space-separated string
    text = sample_text

    # Define a regular expression pattern to match the age
    age_pattern = r'\b\d+\b'

    # Use re.findall to find all occurrences of the pattern in the text
    ages = re.findall(age_pattern, text)

    # If there are multiple occurrences, you can take the first one
    if ages:
        age = int(ages[0])
        # print(f"The age is: {age} years old")
        for i in age_groups.values():
          # print(f"Got values: {i}")
          if (age >= i[0] and age < i[1]):
            # age_group = list(age_groups.keys())[list(age_groups.values()).index(i)]
            age_group = (i[0], i[1])
            # print(f"Setting age_group: {age_group}")
            break

  # Print the extracted information
  # print("Req: ", sheet)
  # print("Region:", region)
  # print("Age Group:", age_group)
  # print("Occasion:", occasion)
  # print("Gender:", gender)
  # print("Category: ", cat)
  return [sheet, region, age_group, occasion, gender, cat]


# In[ ]:


def filter(params, df):
  # print(f"region: {params[1].capitalize()}, occassion: {params[3].capitalize()}, gender: {params[4]}, cat: {params[5].capitalize()}")
  answer = pd.DataFrame()
  # answer = df[(df["Region"].isin([params[0].capitalize()]) & (params[2].capitalize() == df["Occasion"]) & (df["Gender"] == params[3]))]
  for i in range(len(df)):
    # print(f"Got row: region: {df.loc[i, 'Region']}, occ: {df.loc[i, 'Occasion']}, gender: {df.loc[i, 'Gender']}")
    if (df.loc[i, "Region"].capitalize() == params[1].capitalize() or df.loc[i, "Region"] == 'all'):
      # print("correct region")
      if (df.loc[i, "Occasion"].capitalize() == params[3].capitalize() or df.loc[i, "Occasion"] == "all"):
        # print("correct occasion")
        if (df.loc[i, "Gender"] == params[4]):
          # print("Correct gender")
          if (df.loc[i, "Category"].capitalize() == params[5].capitalize() or params[5].capitalize() == "Any"):
            # print("Got row: ", df.loc[i])
            # answer = answer.append([df.loc[i]])
            answer = pd.concat([answer, df.loc[i]], ignore_index=True)
                    
  # print("Got answer: ", answer)
  return answer



def extractImages(df):
  imageNames = []
  nonzero= df[df != 0].stack().values
  # print(nonzero)
  for i in nonzero:
    if (i.endswith(".jpg") and i not in imageNames):
      imageNames.append(i)
  return imageNames

def driver():
    usedf = None
    curGen = None

    df_acc, df_dress, df_foot = loadData()

    # prompt = input("Enter prompt: ")
    prompt = sys.argv[1]
    # print(f'Got prompt: {prompt}')
    params = main(prompt)
    if (params[4] == 'Unknown' and curGen != None):
        params[4] = curGen
    elif (params[4] == 'Unknown' and curGen == None):
        print("Please specify the gender you want to look for next time")
        return
    else:
        curGen = params[4]
# print(f"df2.head: {df2}")
# print(params)
    if (params[0] == 'footwear'):
        # print("using the footwear dataset")
        usedf =  df_foot
    if (params[0] == 'dress'):
        # print("using the dress dataset")
        usedf = df_dress
    if (params[0] == 'accessories'):
        # print("using the acc dataset")
        usedf = df_acc
# print("Now usedf is: ", usedf.head())
    adf = filter(params, usedf)
    if (len(adf) == 0):
        # print("Previous empty so using entire dataset")
        adf = usedf
    recImages = extractImages(adf)
    # print("Got image names: ", recImages)
# imgfiles = loadImages(recImages)
# # for i in imgfiles:
# #   display(i)
    if (len(recImages) == 0):
        print("No Images for this in the dataset")
    elif (len(recImages) < 3):
        return recImages
# for i in (recImages):
# if (i.endswith("avif")):
# loadImages(i)
# else:
# urlLoadImages(i)
    else:
        return list(np.random.choice(recImages, size=3))
# loadimagelist = np.random.choice(recImages, size=3)
# for i in loadimagelist:
#   if (i.endswith("avif")):
#     loadImages(i)
#   else:
#     urlLoadImages(i)



# # Sample Prompts
# - I want a cool new outfit for diwali (done)
# - I am a guy living in delhi and I am looking for casual footwear (Done)
# - I am a lady living in mumbai and I am looking for formal footwear (done)
# - I am a girl living in pune and I am looking for formal outfit (done)
# - I am a girl living in pune and I am looking accessories to match with my party wear. (done)
# - A man living in south-india is looking for an onam dress (done)
# - A young guy is looking for a casual college outfit (done)
# - A young lady is looking for a formal outfit for office (done)
# - I am a middle-aged man looking for casual comfortable footwear (done)
# - A college going boy looking for accessories.
# 

# # **Extracting Region from the input text**

# In[ ]:

def locations():
    delhi = [
        'Chattarpur',
        'Vasant Kunj',
        'Najafgarh',
        'Saket',
        'Dwarka',
        'Connaught Place',
        'Karol Bagh',
        'Rohini',
        'Lajpat Nagar',
        'Mayur Vihar',
        'Hauz Khas',
        'Paharganj',
        'Malviya Nagar',
        'Pitampura',
        'Green Park',
        'Sarita Vihar',
        'Shahdara',
        'Janakpuri',
        'Noida',
        'Gurgaon'
    ]
    punjab = [
        'Amritsar',
        'Ludhiana',
        'Jalandhar',
        'Patiala',
        'Bathinda',
        'Hoshiarpur',
        'Mohali',
        'Pathankot',
        'Moga',
        'Abohar',
        'Faridkot',
        'Firozpur',
        'Gurdaspur',
        'Kapurthala',
        'Malerkotla',
        'Mansa',
        'Muktsar',
        'Nawanshahr',
        'Phagwara',
        'Sangrur'
    ]
    haryana = [
        'Chandigarh',
        'Faridabad',
        'Gurgaon',
        'Panipat',
        'Ambala',
        'Yamunanagar',
        'Rohtak',
        'Hisar',
        'Karnal',
        'Sonipat',
        'Panchkula',
        'Bhiwani',
        'Sirsa',
        'Jind',
        'Thanesar',
        'Kaithal',
        'Rewari',
        'Palwal',
        'Jagadhri',
        'Ambala Cantonment'
    ]
    rajasthan = [
        'Jaipur',
        'Jodhpur',
        'Udaipur',
        'Ajmer',
        'Kota',
        'Bikaner',
        'Alwar',
        'Bharatpur',
        'Sikar',
        'Pali',
        'Ganganagar',
        'Bhilwara',
        'Kishangarh',
        'Barmer',
        'Tonk',
        'Banswara',
        'Nagaur',
        'Sawai Madhopur',
        'Chittorgarh',
        'Dholpur'
    ]
    gujarat = [
        'Ahmedabad',
        'Surat',
        'Vadodara',
        'Rajkot',
        'Bhavnagar',
        'Jamnagar',
        'Junagadh',
        'Gandhinagar',
        'Anand',
        'Bharuch',
        'Porbandar',
        'Nadiad',
        'Gandhidham',
        'Navsari',
        'Valsad',
        'Mehsana',
        'Surendranagar',
        'Bhuj',
        'Gandeva',
        'Palanpur'
    ]
    maharashtra = [
        'Mumbai',
        'Pune',
        'Nagpur',
        'Thane',
        'Nashik',
        'Aurangabad',
        'Solapur',
        'Amravati',
        'Nanded',
        'Kolhapur',
        'Sangli',
        'Jalgaon',
        'Akola',
        'Latur',
        'Dhule',
        'Ahmednagar',
        'Chandrapur',
        'Parbhani',
        'Jalna',
        'Ichalkaranji'
    ]

    south_india = {
        'karnataka': [
            'Bangalore',
            'Mysore',
            'Hubli',
            'Mangalore',
            'Belgaum',
            'Davanagere',
            'Bellary',
            'Gulbarga',
            'Shimoga',
            'Tumkur',
            'Udupi',
            'Hassan',
            'Bidar',
            'Hospet',
            'Raichur',
            'Dharwad',
            'Kolar',
            'Mandya',
            'Chitradurga',
            'Chikmagalur'
        ],
        'tamil_nadu': [
            'Chennai',
            'Coimbatore',
            'Madurai',
            'Tiruchirappalli',
            'Salem',
            'Tirunelveli',
            'Vellore',
            'Thoothukudi',
            'Nagercoil',
            'Thanjavur',
            'Dindigul',
            'Cuddalore',
            'Erode',
            'Hosur',
            'Tiruppur',
            'Kancheepuram',
            'Karur',
            'Namakkal',
            'Ramanathapuram',
            'Pollachi'
        ],
        'telangana': [
            'Hyderabad',
            'Warangal',
            'Nizamabad',
            'Karimnagar',
            'Ramagundam',
            'Khammam',
            'Mahbubnagar',
            'Nalgonda',
            'Adilabad',
            'Siddipet',
            'Miryalaguda',
            'Jagtial',
            'Nirmal',
            'Kothagudem',
            'Suryapet',
            'Wanaparthy',
            'Mancherial',
            'Kagaznagar',
            'Bhongir',
            'Vikarabad'
        ],
        'south-india' : [
            'south-india'
        ],
        'kerela' : [
            'thiruvananthapuram',
            'cochin',
        ]
    }

    west_bengal = [
        'Kolkata',
        'Howrah',
        'Durgapur',
        'Asansol',
        'Siliguri',
        'Darjeeling',
        'Malda',
        'Jalpaiguri',
        'Kharagpur',
        'Haldia',
        'Berhampur',
        'Balurghat',
        'Raniganj',
        'Cooch Behar',
        'Alipurduar',
        'Purulia',
        'Bankura',
        'Medinipur',
        'Serampore',
        'Bardhaman'
    ]
    bihar = [
        'Patna',
        'Gaya',
        'Bhagalpur',
        'Muzaffarpur',
        'Purnia',
        'Darbhanga',
        'Arrah',
        'Begusarai',
        'Katihar',
        'Chhapra',
        'Danapur',
        'Saharsa',
        'Hajipur',
        'Sasaram',
        'Bettiah',
        'Motihari',
        'Bagaha',
        'Kishanganj',
        'Jamalpur',
        'Buxar'
    ]
    odisha = [
        'Bhubaneswar',
        'Cuttack',
        'Rourkela',
        'Brahmapur',
        'Puri',
        'Sambalpur',
        'Balasore',
        'Bhadrak',
        'Baripada',
        'Jeypore',
        'Jharsuguda',
        'Angul',
        'Bargarh',
        'Paradip',
        'Bhawanipatna',
        'Dhenkanal',
        'Barbil',
        'Kendujhar',
        'Jagatsinghpur',
        'Nayagarh'
    ]
    madhya_pradesh = [
        'Bhopal',
        'Indore',
        'Jabalpur',
        'Gwalior',
        'Ujjain',
        'Sagar',
        'Dewas',
        'Satna',
        'Ratlam',
        'Rewa',
        'Katni',
        'Chhindwara',
        'Burhanpur',
        'Khandwa',
        'Morena',
        'Bhind',
        'Guna',
        'Shivpuri',
        'Damoh',
        'Mandsaur'
    ]
    chhattisgarh = [
        'Raipur',
        'Bhilai',
        'Durg',
        'Bilaspur',
        'Korba',
        'Raigarh',
        'Jagdalpur',
        'Ambikapur',
        'Rajnandgaon',
        'Chirmiri',
        'Dhamtari',
        'Janjgir',
        'Kanker',
        'Kawardha',
        'Mahasamund',
        'Naila Janjgir',
        'Tilda Newra',
        'Bhatapara',
        'Mungeli',
        'Baloda Bazar'
    ]
    assam = [
        'Guwahati',
        'Silchar',
        'Dibrugarh',
        'Jorhat',
        'Nagaon',
        'Tinsukia',
        'Tezpur',
        'Karimganj',
        'Sivasagar',
        'Barpeta',
        'Goalpara',
        'Dhubri',
        'Nalbari',
        'Diphu',
        'North Lakhimpur',
        'Bongaigaon',
        'Hailakandi',
        'Morigaon',
        'Dhemaji',
        'Kokrajhar'
    ]
    arunachal_pradesh = [
        'Itanagar',
        'Naharlagun',
        'Tawang',
        'Bomdila',
        'Pasighat',
        'Khonsa',
        'Anini',
        'Roing',
        'Ziro',
        'Aalo',
        'Tezu',
        'Changlang',
        'Seppa',
        'Yingkiong',
        'Bhalukpong',
        'Daporijo',
        'Along',
        'Namsai',
        'Tuting',
        'Hayuliang'
    ]
    manipur = [
        'Imphal',
        'Thoubal',
        'Bishnupur',
        'Churachandpur',
        'Senapati',
        'Ukhrul',
        'Jiribam',
        'Kakching',
        'Tamenglong',
        'Chandel',
        'Kangpokpi',
        'Noney',
        'Tengnoupal',
        'Pherzawl',
        'Kamjong',
        'Kangpokpi',
        'Jiribam',
        'Kakching',
        'Kangchup',
        'Samurou'
    ]
    meghalaya = [
        'Shillong',
        'Tura',
        'Jowai',
        'Nongstoin',
        'Williamnagar',
        'Baghmara',
        'Resubelpara',
        'Khliehriat',
        'Mairang',
        'Nongpoh',
        'Amlarem',
        'Mawkyrwat',
        'Khonjoy',
        'Sohra',
        'Dawki',
        'Cherrapunji',
        'Jakrem',
        'Mendipathar',
        'Songsak',
        'Nongpoh'
    ]
    mizoram = [
        'Aizawl',
        'Lunglei',
        'Saiha',
        'Champhai',
        'Serchhip',
        'Kolasib',
        'Lawngtlai',
        'Demagiri',
        'Thenzawl',
        'Hnahthial',
        'Khawhai',
        'N.Cachar Hills',
        'Saitual',
        'Aibawk',
        'Zawlnuam',
        'Biate',
        'Tlabung',
        'Tlangnuam',
        'Phullen',
        'Tlabung'
    ]
    nagaland = [
        'Kohima',
        'Dimapur',
        'Mokokchung',
        'Tuensang',
        'Wokha',
        'Zunheboto',
        'Mon',
        'Phek',
        'Kiphire',
        'Longleng',
        'Peren',
        'Noklak',
        'Jalukie',
        'Chumukedima',
        'Zunheboto',
        'Tseminyu',
        'Pfutsero',
        'Chuchuyimlang',
        'Kohima Village',
        'Alichen'
    ]
    goa = [
        'Panaji',
        'Margao',
        'Vasco da Gama',
        'Mapusa',
        'Ponda',
        'Calangute',
        'Curchorem',
        'Sanguem',
        'Bicholim',
        'Cuncolim',
        'Valpoi',
        'Canacona',
        'Quepem',
        'Colva',
        'Benaulim',
        'Dabolim',
        'Anjuna',
        'Pernem',
        'Arambol',
        'Mormugao'
    ]
    andaman_nicobar = [
        'Port Blair',
        'Havelock Island',
        'Neil Island',
        'Diglipur',
        'Rangat',
        'Mayabunder',
        'Wandoor',
        'North Bay Island',
        'Little Andaman',
        'Car Nicobar',
        'Great Nicobar',
        'Long Island',
        'Baratang Island',
        'Campbell Bay',
        'Rangat',
        'Neil Island',
        'Diglipur',
        'Mangrove Creek',
        'Interview Island',
        'Hut Bay'
    ]
    chandigarh = [
        'Chandigarh'
    ]
    lakshadweep = [
        'Kavaratti',
        'Agatti',
        'Amini',
        'Andrott',
        'Bitra',
        'Chetlat',
        'Kadmat',
        'Kalpeni',
        'Kiltan',
        'Minicoy',
        'Bangaram',
        'Bithra',
        'Cheriyam',
        'Kavaratti',
        'Kadmat',
        'Kalpeni',
        'Kavaratti',
        'Kadmat',
        'Kavaratti',
        'Kadmat'
    ]
    puducherry = [
        'Puducherry',
        'Karaikal',
        'Mahe',
        'Yanam'
    ]
    dadra_nagar_haveli = [
        'Silvassa',
        'Dadra',
        'Nagar Haveli',
        'Dadra and Nagar Haveli'
    ]



    city_states = {}

# Creating the dictionary for Delhi
    for city in delhi:
        city_states[city.lower()] = "delhi"

# Creating the dictionary for Punjab
    for city in punjab:
        city_states[city.lower()] = "punjab"

# Creating the dictionary for Haryana
    for city in haryana:
        city_states[city.lower()] = "haryana"

# Creating the dictionary for Rajasthan
    for city in rajasthan:
        city_states[city.lower()] = "rajasthan"

# Creating the dictionary for Gujarat
    for city in gujarat:
        city_states[city.lower()] = "gujarat"

# Creating the dictionary for Maharashtra
    for city in maharashtra:
        city_states[city.lower()] = "maharashtra"

# Creating the dictionary for South India (Karnataka, Tamil Nadu, Telangana)
    for state, cities in south_india.items():
        city_states[state] = 'south-india'
        for city in cities:
            city_states[city.lower()] = "south-india"

# Creating the dictionary for West Bengal
    for city in west_bengal:
        city_states[city.lower()] = "west bengal"

# Creating the dictionary for Bihar
    for city in bihar:
        city_states[city.lower()] = "bihar"

# Creating the dictionary for Odisha
    for city in odisha:
        city_states[city.lower()] = "odisha"

# Creating the dictionary for Madhya Pradesh
    for city in madhya_pradesh:
        city_states[city.lower()] = "madhya pradesh"

# Creating the dictionary for Chhattisgarh
    for city in chhattisgarh:
        city_states[city.lower()] = "chhattisgarh"

# Creating the dictionary for Assam
    for city in assam:
        city_states[city.lower()] = "assam"

# Creating the dictionary for Arunachal Pradesh
    for city in arunachal_pradesh:
        city_states[city.lower()] = "arunachal pradesh"

# Creating the dictionary for Manipur
    for city in manipur:
        city_states[city.lower()] = "manipur"

# Creating the dictionary for Meghalaya
    for city in meghalaya:
        city_states[city.lower()] = "meghalaya"

# Creating the dictionary for Mizoram
    for city in mizoram:
        city_states[city.lower()] = "mizoram"

# Creating the dictionary for Nagaland
    for city in nagaland:
        city_states[city.lower()] = "nagaland"

# Creating the dictionary for Goa
    for city in goa:
        city_states[city.lower()] = "goa"

# Creating the dictionary for Andaman and Nicobar Islands
    for city in andaman_nicobar:
        city_states[city.lower()] = "andaman and nicobar islands"

# Creating the dictionary for Chandigarh
    for city in chandigarh:
        city_states[city.lower()] = "chandigarh"

# Creating the dictionary for Lakshadweep
    for city in lakshadweep:
        city_states[city.lower()] = "lakshadweep"

# Creating the dictionary for Puducherry
    for city in puducherry:
        city_states[city.lower()] = "puducherry"

# Creating the dictionary for Dadra and Nagar Haveli
    for city in dadra_nagar_haveli:
        city_states[city.lower()] = "dadra and nagar haveli"

    return city_states

if __name__ == "__main__":
    urlList = driver()
    print(json.dumps(urlList))
