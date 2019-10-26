float y_slicing_Plane(vec3 p, float y_of_plane){
    return -(p.y - y_of_plane);
}

float z_ground_Plane(vec3 p, float z_of_plane){
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
    vec3 new_position =  p-c*clamp (round(p/c),-l,l);
    return new_position;  
}

































































