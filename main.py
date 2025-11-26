import os
import sys

def main():
    while True:
        print("\n--- Self Learning Car Menu ---")
        print("1. Draw Track (track_maker.py)")
        print("2. Train Car (train.py)")
        print("3. Watch AI (play.py)")
        print("4. Race vs AI (race.py)")
        print("5. Install Requirements")
        print("6. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            os.system("python track_maker.py")
        elif choice == '2':
            os.system("python train.py")
        elif choice == '3':
            os.system("python play.py")
        elif choice == '4':
            os.system("python race.py")
        elif choice == '5':
            os.system("pip install -r requirements.txt")
        elif choice == '6':
            sys.exit()
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
