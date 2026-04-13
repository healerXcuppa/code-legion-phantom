// C++ Assignment (Week1: Variables)
// Write a C++ program that:
// 1. Ask user for their name.
// 2. Asks user for their age.
// 3. Prints both inputs in a single Line

#include <iostream>
using namespace std;
int main(){
    string name;
    int age;
    
    // Asking user for their name and printing name confirmation.
    cout << endl; 
    cout << "Enter your name: ";
    cin >> name;
    cout<<"Name recorded: " << name << endl; 

    // Asking user for their age and printing age confirmation.
    cout << "Enter your age: ";
    cin >> age;
    cout<<"Age recorded: " << age << endl;

    // Final Output
    cout << "Your name is " << name << " and you are " << age << " years old." << endl;
    return 0;
}