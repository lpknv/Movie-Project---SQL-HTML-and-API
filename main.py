from movies import main

if __name__ == "__main__":
    try:
        main()
    # print some nice message when quitting the program using keyboard interrupt
    except KeyboardInterrupt:
        print("See ya!")