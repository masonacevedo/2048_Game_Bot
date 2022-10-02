#include <iostream>

class Board {
    public:
        int board [4][4] = {{0,0,0,0},{0,0,0,0},{0,0,0,0},{0,0,0,0}};        
        void printNice(){
            for (int i = 0; i < sizeof(board)/sizeof(board[0]); i++){
                for (int j = 0; j < sizeof(board[0])/sizeof(int); j++){
                    std::cout << board[i][j] << " ";
                }
                std::cout << "\n";
            }
            std::cout << std::endl;
        }
};

int main(){
    // std::cout << "Hello world!" << std::endl;
    Board myBoard;
    myBoard.printNice();

    return 0;
}