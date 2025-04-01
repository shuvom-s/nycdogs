import pandas as pd
import json
import os

def preprocess_data():
    print("Loading NYC dogs dataset...")
    # Load the dataset
    df_dogs = pd.read_csv('nycdogs.csv')
    
    # Deduplicate the dataset
    df_dogs_unique = df_dogs.drop_duplicates()
    
    # Save deduplicated dataset
    df_dogs_unique.to_csv('app/data/nycdogs_unique.csv', index=False)
    print(f"Deduplicated dataset saved with {len(df_dogs_unique)} rows (from original {len(df_dogs)} rows)")
    
    # Filter for breeds with at least 100 dogs
    breed_counts = df_dogs_unique['BreedName'].value_counts()
    valid_breeds = breed_counts[breed_counts >= 100].index.tolist()
    
    # Filter for names with at least 100 dogs
    name_counts = df_dogs_unique['AnimalName'].value_counts()
    valid_names = name_counts[name_counts >= 100].index.tolist()
    
    # Create dictionaries to store counts by zip code
    breed_data = {}
    for breed in valid_breeds:
        breed_by_zip = df_dogs_unique[df_dogs_unique['BreedName'] == breed]['ZipCode'].value_counts().to_dict()
        breed_data[breed] = breed_by_zip
    
    name_data = {}
    for name in valid_names:
        name_by_zip = df_dogs_unique[df_dogs_unique['AnimalName'] == name]['ZipCode'].value_counts().to_dict()
        name_data[name] = name_by_zip
    
    # Save breed and name data as JSON
    os.makedirs('app/data', exist_ok=True)
    
    with open('app/data/breed_data.json', 'w') as f:
        json.dump(breed_data, f)
    
    with open('app/data/name_data.json', 'w') as f:
        json.dump(name_data, f)
    
    with open('app/data/valid_breeds.json', 'w') as f:
        json.dump(valid_breeds, f)
    
    with open('app/data/valid_names.json', 'w') as f:
        json.dump(valid_names, f)
    
    print(f"Processed {len(valid_breeds)} breeds and {len(valid_names)} names with at least 100 dogs each")
    return valid_breeds, valid_names

if __name__ == "__main__":
    preprocess_data() 