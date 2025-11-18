def isLeapYear(year):
 if(year % 100 != 0 and year % 4 == 0):
    return True
 elif(year %  100 == 0 and year % 400 == 0):
    return True
 else:
    return False
    
### user validation  loop
while True: 
    try:
        currentYear =int(input("please enter a year: "))
        if(isLeapYear(currentYear)):
            print(currentYear, 'is a valid leap year. ')
            break
        else:
            print(currentYear, "is not a valid leap year")
            
    except:
        print("Pleease Try Again!")
        
        