#include <iostream>

int main(int argc, char* argv[]) {
    int data_num;
    std::cin >> data_num;

    int sum = 0;
    int tmp = 0;
    for (int i=0; i < data_num; i++) {
        std::cin >> tmp;
        sum = sum + tmp;
    }
    std::cout << sum << std::endl;

    return 0;
}
