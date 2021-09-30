import requests
import base64
import json


# Set up this fields to match your needs

fileExtension = ".png" # file extension of your images
mimeType = "image/png" # make sure it matches with yoru file type
metaDataFileName = "metadata.json" # metadata filename
apiKey = "" # apiKey provided from the website
nftprojectid = "" # project Id provided from the website
nftCount = 10000 # how many files to upload
uploadURL = f'https://api.nft-maker.io/UploadNft/{apiKey}/{nftprojectid}' # endpoint for uploading files
log = [] # an array to save file upload logs, for detecting errors after the upload

# Sample Metadata I created on the nft-maker
# {
#   "721": {
#     "<policy_id>": { => inserted by NFTMaker
#       "<asset_name>": { => inserted by NFTMaker
#         "name": "<name_with_hashtag>",
#         "image": "<ipfs_link>", => inserted by NFTMaker
#         "mediaType": "<mime_type>",
#         "website": "https://avocadobreakfastclub.com/", => inserted by NFTMaker, so we do not have specify it on every upload
#         "attributes": {
#           "Background": "<Background>",
#           "Head": "<Head>",
#           "Face": "<Face>",
#           "Shell": "<Shell>",
#           "Pulp": "<Pulp>",
#           "Tattoo": "<Tattoo>",
#           "Stone": "<Stone>",
#           "Character": "<Character>"
#         }
#       }
#     }
#   }
# }

# Read metadata (contains metadata for all images)
# Be careful that this file needs to be at same location for this script to work.
with open(metaDataFileName) as f:
    metadata = json.load(f)
print("metadata:", metaDataFileName, "read.")
print("Uploading to:", uploadURL)

# Loop through files, set their attributes from metadata.json and upload
for i in range(nftCount):
    
    # You should change below code with your attributes.
    # p.s this could be written better..
    Background = metadata[str(i)]['attributes'][0]['value']
    Shell = metadata[str(i)]['attributes'][1]['value']
    Pulp = metadata[str(i)]['attributes'][2]['value']
    Tattoo = metadata[str(i)]['attributes'][3]['value']
    Stone = metadata[str(i)]['attributes'][4]['value']
    Character = metadata[str(i)]['attributes'][5]['value']
    Face = metadata[str(i)]['attributes'][6]['value']
    Head = metadata[str(i)]['attributes'][7]['value']
    
    if(i < 10):
        assetName = '000'+str(i)
    elif(i < 100):
        assetName = '00'+str(i)
    elif(i < 1000):
        assetName = '0'+str(i)
    else:
        assetName = str(i)
    
    # Read each file and convert to Base64 format.
    # Files are formatted as 0.png, 1.png ...
    file = f'{str(i)}{fileExtension}'
    with open(file, 'rb') as binary_file:
        binary_file_data = binary_file.read()
        base64_encoded_data = base64.b64encode(binary_file_data)
        base64_message = base64_encoded_data.decode('utf-8')
    
    # Set up parameters for POST request. You should change this value.
    params = {
        "assetName": assetName, # If you set up a prefix in your project, you omit the prefix here, if not add prefix as well
        "previewImageNft": {
            "mimetype": mimeType,
            "fileFromBase64": base64_message,
            "metadataPlaceholder": [
                {
                    "name": "Background",
                    "value": Background
                },
                {
                    "name": "Shell",
                    "value": Shell
                },
                {
                    "name": "Pulp",
                    "value": Pulp
                },
                {
                    "name": "Tattoo",
                    "value": Tattoo
                },
                {
                    "name": "Stone",
                    "value": Stone
                },
                {
                    "name": "Character",
                    "value": Character
                },
                {
                    "name": "Face",
                    "value": Face
                },
                {
                    "name": "Head",
                    "value": Head
                },
                {
                    "name": "name_with_hashtag",
                    "value": metadata[str(i)]['name'] #coming directly form metadata.json
                }
            ]
        }
    }

    # Send HTTP Post request.
    headers = {'Content-Type': 'application/json'}
    try:
        r = requests.post(uploadURL, json=params)
        print(str(i) + ' : SUCCESS!')
        log.append(str(i) + ' : SUCCESS!')
    except:
        print(str(i) + ' : FAILED!')
        log.append(str(i) + ' : FAILED!')

# Print logs into file. 
# p.s this could be improved,
# as log file is not created if you suddenly stop the execution ,i.e CTRL+C
with open("log.txt", "w") as text_file:
    print(log, file=text_file)
