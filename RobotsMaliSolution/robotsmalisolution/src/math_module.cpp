#include <iostream>
#include <complex>
#include "math_module.hpp"

std::complex<double> get_middle(std::complex<double> complex_1, std::complex<double> complex_2){

std::complex<double> middle = (complex_1 + complex_2)/2.0;

return middle;

}
void translation(std::complex<double>& translation_point, bool vtranslation , double vprecision , double hprecision ) {

    double x = real(translation_point);
    double y = imag(translation_point);


    if (vtranslation) {

        if (x < 0 && y < 0) {

            y -= vprecision;

        }
        
        else {
            y += vprecision;
            
        }
    }

    else {

        if (x < 0) {

            x -= hprecision;
            
        }

        else {
            
            x += hprecision;
            
        } 
    }

    translation_point = std::complex<double>(x,y);
}