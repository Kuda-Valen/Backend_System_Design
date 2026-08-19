
from user_info import User
from authentication import signup, login, forgot_signin

if __name__ == "__main__":
    user = User()

    while True:
        print("== Zolax ==")
        print("1. Login")
        print("2. Sign UP")
        print("3. Forgot Login Details")
        print("4. Exit")

        try:
            option = int(input("\nChoose an Option: "))

            if option == 1:
                login()

            elif option == 2:
                signup()

            elif option == 3:
                forgot_signin()

            elif option == 4: 
                print("\nExiting!!..")

            else:
                print("\nInvalid input. Choose a Valid input..")

        except ValueError as e:
            print(f"\nEncountered input error: {e}")

