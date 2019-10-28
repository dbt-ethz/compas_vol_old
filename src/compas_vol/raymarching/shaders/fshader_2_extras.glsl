float y_slicing_Plane(vec3 p, float y_of_plane){
    return p.y - y_of_plane;
}

float z_slicing_Plane(vec3 p, float z_of_plane){
    return p.z - z_of_plane;
}

float bounding_sphere_primitive(vec3 p, vec3 center, float radius){
    return length(p - center) - radius;
}

float displacement (in vec3 p, in float frequence, in float magnitude){ // frequence = 2.5, magnitude = 0.2
    float displacement = magnitude * sin(frequence* p.x) * sin(frequence* p.y)*sin(frequence * p.z);
    return displacement;
}

vec3 twist(in vec3 p, in float k){ // twist along z axis 
    float c = cos(k*p.y);
    float s = sin(k*p.y);
    mat2  m = mat2(c,-s,s,c);
    vec3  new_position = vec3(m*p.xz,p.y);
    return new_position;
}

vec3 infinite_repetition(in vec3 p, in vec3 c){
    vec3 new_position = mod(p+0.5*c,c)-0.5*c;
    return new_position;  
}

vec3 finite_repetition(in vec3 p, in vec3 c, in vec3 l){
    vec3 new_position =  p - c*clamp (round(p/c),-l,l);
    return new_position;  
}

float ripples_sin(in vec3 p, float start_dist, float amplitude, float frequency){ //0.02, 50 
    start_dist -= amplitude* 0.5;
    float ripples_z = p.z; // - height * p.x * p.x; //along they y-height, minus parabola for curve
    return start_dist - amplitude * abs(sin(ripples_z * frequency)) ;// * (1 - smoothstep(0.0, 0.15, abs(ripples_y)));
}

float ripples_fract(in vec3 p, float start_dist, float amplitude, float frequency){
    start_dist -= amplitude* 0.5;
    float dz = fract(p.z * frequency);
    float curve = smoothstep( 0., 0.25, dz*(1 - dz));
    return start_dist - curve * amplitude ;
}

float remap(in float value,in float  start1,in float  stop1, in float  start2, in float stop2){
    return  start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1));
}

vec3 staircase_z(in vec3 p, in float frequency){
    // float f2 = floor (p.z * frequency)  / frequency ;
    // float f3 = p.z - f2;
    // float f4 = pow(f3  - 0.5 , 5) * pow(2,6)  + 0.5;
    // float z_scaled = f2 + f4;
    float z_scaled = floor(p.z * frequency) / frequency ;
    return vec3(p.x, p.y, z_scaled);
} 

float shell(in float start_dist, in float thickness){
    return abs(start_dist + thickness) - thickness;
}

float smooth_union(in float a, in float b, float k){
    float h = max(k - abs(a-b), 0.0);
    return min(a,b) - h*h/(k*4.0);
}

float smooth_subtraction(in float a, in float b, float k){
    float h = max(k - abs(a-b), 0.0);
    return max(a,b) + h*h/(k*4.0);
}

float segmentation_offset (in float start_dist, in float shell_thickness){
    float result = 1000;  // big number
    float current_shell = 0;
    float current_offset = 0;

    for (int i=0; i<25; i++){
        current_shell = shell(start_dist + current_offset, shell_thickness);
        current_offset += shell_thickness * 3.5;
        result = min(result, current_shell);
        if (current_offset < start_dist) break;
    }
    return result;
}

// fast version
float segmentation_plane_z(in vec3 p, in float start_dist, in float thickness, in int iterations_num, in float start_z){
    vec3 pos_repeated = vec3(p.x, p.y, mod(p.z, thickness * 3)  + p.z ); // REPETITION OF ELEMENTS, mod, fract
    float slicing_plane = shell(p.z - pos_repeated.z , thickness);
    float slice = smooth_subtraction(start_dist, slicing_plane, 0.015);
    return slice;
}

// // slow version 
// float segmentation_plane_z(in vec3 p, in float start_dist, in float thickness, in int iterations_num, in float start_z){
//     float result =  1000;  // big number
//     float current_height_z = start_z;
//     for (int i=0; i<iterations_num; i++){
//         float slicing_plane = shell(p.z - pos_repeated.z , thickness);
//         float slice = smooth_subtraction(start_dist, slicing_plane, 0.015);
//         current_height_z += 3.5 * thickness;
//         result = min(result, slice);
//     }
//     return result;
// }































































































