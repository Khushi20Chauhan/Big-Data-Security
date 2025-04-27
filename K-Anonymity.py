import pandas as pd
from collections import defaultdict

def load_dataset():
    # Original dataset
    data = {
        'ZIP Code': [13053, 13053, 13068, 13053, 13068, 13053],
        'Age': [29, 29, 45, 31, 47, 33],
        'Gender': ['F', 'F', 'M', 'M', 'M', 'M'],
        'Condition': ['Diabetes', 'Cancer', 'Hypertension', 'Flu', 'Asthma', 'Allergy']
    }
    return pd.DataFrame(data)

def enforce_k_anonymity(df, k):
    anonymized_df = df.copy()
    
    # Try just ZIP generalization first
    anonymized_df['ZIP Code'] = anonymized_df['ZIP Code'].astype(str).str[:-1] + 'x'
    groups = anonymized_df.groupby(['ZIP Code', 'Age', 'Gender']).size()
    
    if all(groups >= k):
        return anonymized_df
    
    # If not, try age generalization
    anonymized_df['Age'] = (anonymized_df['Age'] // 10) * 10
    groups = anonymized_df.groupby(['ZIP Code', 'Age', 'Gender']).size()
    
    if all(groups >= k):
        return anonymized_df
    
    # If still not enough, generalize ZIP further
    anonymized_df['ZIP Code'] = anonymized_df['ZIP Code'].str[:3] + 'xx'
    return anonymized_df

def display_menu():
    print("\n=== K-Anonymity Tool ===")
    print("1. View original dataset")
    print("2. Apply 2-anonymity")
    print("3. Apply 3-anonymity")
    print("4. Apply custom k-anonymity")
    print("5. Compare different k-values")
    print("6. Exit")
    return input("Please enter your choice (1-6): ")

def main():
    df = load_dataset()
    
    while True:
        choice = display_menu()
        
        if choice == '1':
            print("\nOriginal Dataset:")
            print(df)
            print("\nGroup counts in original data:")
            print(df.groupby(['ZIP Code', 'Age', 'Gender']).size())
            
        elif choice == '2':
            k2_df = enforce_k_anonymity(df, 2)
            print("\nData with 2-anonymity:")
            print(k2_df)
            print("\nGroup counts:")
            print(k2_df.groupby(['ZIP Code', 'Age', 'Gender']).size())
            
        elif choice == '3':
            k3_df = enforce_k_anonymity(df, 3)
            print("\nData with 3-anonymity:")
            print(k3_df)
            print("\nGroup counts:")
            print(k3_df.groupby(['ZIP Code', 'Age', 'Gender']).size())
            
        elif choice == '4':
            try:
                k = int(input("Enter desired k-value: "))
                if k < 1:
                    print("k must be at least 1")
                    continue
                custom_df = enforce_k_anonymity(df, k)
                print(f"\nData with {k}-anonymity:")
                print(custom_df)
                print("\nGroup counts:")
                print(custom_df.groupby(['ZIP Code', 'Age', 'Gender']).size())
            except ValueError:
                print("Please enter a valid integer")
                
        elif choice == '5':
            print("\nComparison of different k-values:")
            
            print("\nOriginal data group sizes:")
            print(df.groupby(['ZIP Code', 'Age', 'Gender']).size())
            
            print("\n2-anonymity group sizes:")
            k2_df = enforce_k_anonymity(df, 2)
            print(k2_df.groupby(['ZIP Code', 'Age', 'Gender']).size())
            
            print("\n3-anonymity group sizes:")
            k3_df = enforce_k_anonymity(df, 3)
            print(k3_df.groupby(['ZIP Code', 'Age', 'Gender']).size())
            
        elif choice == '6':
            print("Exiting program...")
            break
            
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
            
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()