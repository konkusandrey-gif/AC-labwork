#include <stdio.h>
#include <windows.h> 


void gotoxy(int x, int y) {
    COORD coord;
    coord.X = x - 1; 
    coord.Y = y - 1;
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), coord);
}

int main() {
    
    int x = 40;
    int y = 12;

    
    int length = 1;     
    int step_count = 0; 
    int direction = 0;  
    
    
    int turn_count = 0; 

    
    system("cls");

   
    gotoxy(x, y);
    printf("*");

    
    while (1) {
        
        
        switch (direction) {
            case 0: x++; break; 
            case 1: y++; break; 
            case 2: x--; break; 
            case 3: y--; break; 
        }

        
        if (x < 1 || x > 80 || y < 1 || y > 24) {
            break; 

        
        gotoxy(x, y);
        printf("*");
        
       
        Sleep(50); 

        step_count++;

        
        if (step_count == length) {
            step_count = 0;     
            direction++;        
            if (direction > 3) direction = 0; 
            turn_count++;
            
            
            if (turn_count % 2 == 0) {
                length++;
            }
        }
    }

    
    gotoxy(1, 24);
    return 0;
}