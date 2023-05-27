#ifndef MATH_MODULE_HPP
#define MATH_MODULE_HPP

#include <iostream>
#include <complex>

std::complex<double> get_middle(std::complex<double>& complex_1, std::complex<double>& complex_2){

std::complex<double> middle = (complex_1 + complex_2)/2.0;

return middle;

}
std::complex<double> translation(std::complex<double>& translation_point, bool vtranslation = false , double vprecision = 1.0 , double hprecision = 1.0 ) {

    double x =translation_point.real();
    double y = translation_point.imag();


    if (vtranslation) {

        if (x < 0 && y < 0) 

            y -= vprecision;
        
        else 
            y += vprecision;
            
    }

    else {

        if (x < 0) 

            x -= hprecision;
        else 
            
            x += hprecision;
    }

    return std::complex<double>(x,y);
}
#endif
