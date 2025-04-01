import pandas as pd
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns

def preprocess_data():
    print("Loading NYC dogs dataset...")
    # Load the dataset
    df_dogs = pd.read_csv('nycdogs.csv')
    
    # Check columns
    print("Dataset columns:", df_dogs.columns.tolist())
    print("Total rows before deduplication:", len(df_dogs))
    
    # Deduplicate the dataset
    df_dogs_unique = df_dogs.drop_duplicates()
    print("Total rows after deduplication:", len(df_dogs_unique))
    
    # Save deduplicated dataset
    os.makedirs('data', exist_ok=True)
    df_dogs_unique.to_csv('data/nycdogs_unique.csv', index=False)
    
    # Count breeds and filter for those with at least 100 dogs
    breed_counts = df_dogs_unique['BreedName'].value_counts()
    popular_breeds = breed_counts[breed_counts >= 100]
    print(f"\nFound {len(popular_breeds)} breeds with at least 100 dogs")
    print("Top 10 breeds:")
    print(popular_breeds.head(10))
    
    # Count names and filter for those with at least 100 dogs
    name_counts = df_dogs_unique['AnimalName'].value_counts()
    popular_names = name_counts[name_counts >= 100]
    print(f"\nFound {len(popular_names)} names with at least 100 dogs")
    print("Top 10 names:")
    print(popular_names.head(10))
    
    # Create data files for popular breeds and names
    popular_breeds_dict = {}
    for breed in popular_breeds.index:
        breed_df = df_dogs_unique[df_dogs_unique['BreedName'] == breed]
        zipcode_counts = breed_df['ZipCode'].value_counts().to_dict()
        popular_breeds_dict[breed] = {
            'total_count': int(popular_breeds[breed]),
            'zipcode_counts': zipcode_counts
        }
    
    popular_names_dict = {}
    for name in popular_names.index:
        name_df = df_dogs_unique[df_dogs_unique['AnimalName'] == name]
        zipcode_counts = name_df['ZipCode'].value_counts().to_dict()
        popular_names_dict[name] = {
            'total_count': int(popular_names[name]),
            'zipcode_counts': zipcode_counts
        }
    
    # Save to JSON files
    with open('data/popular_breeds.json', 'w') as f:
        json.dump(popular_breeds_dict, f)
    
    with open('data/popular_names.json', 'w') as f:
        json.dump(popular_names_dict, f)
    
    print("\nData preprocessing complete. Files saved to data/ directory")
    
    # Create example visualizations
    create_example_visualizations(df_dogs_unique, list(popular_breeds.index)[:5], list(popular_names.index)[:5])
    
    return popular_breeds_dict, popular_names_dict

def create_example_visualizations(df, top_breeds, top_names):
    print("\nCreating example visualizations...")
    os.makedirs('examples', exist_ok=True)
    
    # Plot for a few top breeds
    for breed in top_breeds:
        print(f"Creating visualization for breed: {breed}")
        breed_df = df[df['BreedName'] == breed]
        
        # Count by zipcode
        zipcode_counts = breed_df['ZipCode'].value_counts().reset_index()
        zipcode_counts.columns = ['ZipCode', 'Count']
        
        # Create plot
        plt.figure(figsize=(12, 8))
        sns.barplot(x='ZipCode', y='Count', data=zipcode_counts.head(15))
        plt.title(f'Distribution of {breed} by NYC Zip Code (Top 15)')
        plt.xlabel('Zip Code')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'examples/{breed.replace("/", "_")}_distribution.png')
        plt.close()
    
    # Plot for a few top names
    for name in top_names:
        print(f"Creating visualization for name: {name}")
        name_df = df[df['AnimalName'] == name]
        
        # Count by zipcode
        zipcode_counts = name_df['ZipCode'].value_counts().reset_index()
        zipcode_counts.columns = ['ZipCode', 'Count']
        
        # Create plot
        plt.figure(figsize=(12, 8))
        sns.barplot(x='ZipCode', y='Count', data=zipcode_counts.head(15))
        plt.title(f'Distribution of Dogs Named {name} by NYC Zip Code (Top 15)')
        plt.xlabel('Zip Code')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'examples/{name}_distribution.png')
        plt.close()
    
    print("Example visualizations created in examples/ directory")

if __name__ == "__main__":
    preprocess_data() 