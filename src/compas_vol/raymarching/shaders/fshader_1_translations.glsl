// #version 120
#version 140

#ifdef GL_ES
precision mediump float;
#endif

#define object_max_num    30 // CAREFUL, MEMORY LIMITED
#define geom_data_max_num 200
#define max_num_of_children 30
#define max_num_of_geom_data 30 // attention should be at least bigger than max_num_of_children

#define resolution_of_texture 1024

///---------------------------------------------------------------- INPUTS
uniform vec2 u_resolution;
uniform vec3 camera_POS;
uniform vec3 camera_START_POS;
uniform float osg_FrameTime;

// v_data
uniform float[object_max_num] v_indices;  
uniform float[object_max_num] v_ids;   
uniform float[object_max_num] v_data_count_per_object;  
uniform float[geom_data_max_num] v_object_geometries_data;  

uniform float y_slice;
uniform int display_target_object;
// uniform float slider_value;

///---------------------------------------------------------------- 
// list of all objects that will be filled in with values 
float[object_max_num] objects_values = v_indices; // We initialize this to some value so that it doesnt give a warnign
                                                  // that it might be used before it is initialized

///---------------------------------------------------------------- SDF FUNCTIONS (from compas-vol)
///// PRIMITIVES 
#define VolSphere_id 100
#define VolBox_id 101
#define VolTorus_id 102
#define VolCylinder_id 103

float random (vec2 st) {
    return fract(sin(dot(st.xy, vec2(12.9898,78.233)))* 43758.5453123);
}

vec3 animate_point(in int current_index){
    float magnitude = random (vec2(current_index))  * 5.+ 1.;
    float frequency1 = random (vec2(current_index/3.56))  * 1.3  + 0.1;
    float offset  = random (vec2(current_index/3.56))  * 6.;
    float frequency = frequency1;
    // frequency *=  slider_value;
    return vec3(sin(osg_FrameTime * frequency) * magnitude, cos(offset +osg_FrameTime * frequency) * magnitude, sin(offset + osg_FrameTime * frequency) * magnitude);
}

float VolPrimitive(in vec3 p, in int id, in int current_index, in float[max_num_of_geom_data] geometry_data){ //current_index only needed for 
    //VolSphere
    if (id == VolSphere_id){
        vec3 center = vec3(geometry_data[0], geometry_data[1], geometry_data[2]);
        center = center + animate_point(current_index) ;
        float radius = geometry_data[3];
        return length(p - center) - radius;
    //VolBox     
    }else if (id == VolBox_id){
        float radius = geometry_data[3];
        vec3 size_xyz= vec3(geometry_data[0], geometry_data[1], geometry_data[2]);
        mat4 matrix = mat4( vec4(geometry_data[4], geometry_data[5], geometry_data[6], geometry_data[7]),
                            vec4(geometry_data[8], geometry_data[9], geometry_data[10], geometry_data[11]),
                            vec4(geometry_data[12], geometry_data[13], geometry_data[14], geometry_data[15]),
                            vec4(geometry_data[16], geometry_data[17], geometry_data[18], geometry_data[19]) );

        vec4 pos_transformed =  transpose(matrix) * vec4(p , 1.);
        vec3 d = abs(pos_transformed.xyz) - (size_xyz.xyz * 0.5 - radius);
        return length(max(d, 0.0)) - radius + min(max(d.x,max(d.y,d.z)), 0.0);
    //VolTorus
    }else if (id == VolTorus_id){
        float center_radius = geometry_data[0];
        float section_radius = geometry_data[1];
        mat4 matrix = mat4( vec4(geometry_data[2], geometry_data[3], geometry_data[4], geometry_data[5]),
                            vec4(geometry_data[6], geometry_data[7], geometry_data[8], geometry_data[9]),
                            vec4(geometry_data[10], geometry_data[11], geometry_data[12], geometry_data[13]),
                            vec4(geometry_data[14], geometry_data[15], geometry_data[16], geometry_data[17]) );

        vec4 pos_transformed = transpose(matrix)  * vec4(p , 1.);
        float dxy = length(pos_transformed.xy);
        float d2 = sqrt((dxy - center_radius)*(dxy - center_radius) + pos_transformed.z*pos_transformed.z );
        return d2 - section_radius;
    //VolCylinder
    }else if (id == VolCylinder_id){
        float h = geometry_data[0];
        float r = geometry_data[1];
        mat4 matrix = mat4( vec4(geometry_data[2], geometry_data[3], geometry_data[4], geometry_data[5]),
                            vec4(geometry_data[6], geometry_data[7], geometry_data[8], geometry_data[9]),
                            vec4(geometry_data[10], geometry_data[11], geometry_data[12], geometry_data[13]),
                            vec4(geometry_data[14], geometry_data[15], geometry_data[16], geometry_data[17]) );

        vec4 pos_transformed = transpose(matrix) * vec4(p , 1.);
        float d = length(pos_transformed.xy) - r;
        return max(d, abs(pos_transformed.z) - h/2.);
    } else {
        return 0.;
    }
}

///// COMBINATIONS
#define Union_id 200
#define Intersection_id 201
#define Smooth_Union_id 202

float VolCombination(in int id, in float[max_num_of_geom_data] geometry_data, in int count){
    //Union
    if (id == Union_id){
        float d = 10000.; // very big value
        for (int i=0; i< count; i++){
            float child_dist = objects_values[int(geometry_data[i])];
            d = min(d, child_dist); }
        return d;
    //Intersection
    } else if (id == Intersection_id){
        float d = -10000.; // very small value
        for (int i=0; i<count; i++){
            float child_dist = objects_values[int(geometry_data[i])];
            d = max(d, child_dist); }
        return d;
    //Smooth Union
    } else if (id == Smooth_Union_id){
        float d = 100000.; // very big value
        float r = geometry_data[0];
        // // 
        // // 
        for (int i=1; i<count; i++){
            float child_dist = objects_values[int(geometry_data[i])];
            float a = d;
            float b = child_dist;
            float h = min(max(0.5 + 0.5 * (b - a) / r, 0), 1);
            d = (b * (1 - h) + h * a) - r * h * (1 - h);}
        return d;
    } else {
        return 0.;
    }
}

///// MODIFICATIONS
#define Shell_id 300

float VolModification(in int id, in int index, in float [max_num_of_geom_data] geometry_data){
    // Shell
    if (id == Shell_id){ //// The shell theoretically needs to know the child. But practically it's always the next index 
        float current_dist = objects_values[index+1]; 
        float d = geometry_data[0];
        float s = geometry_data[1];
        return abs(current_dist + (s - 0.5) * d) - d/2.0;
    } else {
        return 0.;
    }
}

///// MICROSTRUCTURES
#define Lattice_id 400
// float VolMicrostructure(in vec3 p, in int id, in int index, in float [max_num_of_geom_data] geometry_data){
    // // Lattice
    // if (id == Lattice_id){ 
    //     float unitcell = geometry_data[0];
    //     float thickness = geometry_data[1];
    //     mat4 matrix = mat4( vec4(geometry_data[2], geometry_data[3], geometry_data[4], geometry_data[5]),
    //                         vec4(geometry_data[6], geometry_data[7], geometry_data[8], geometry_data[9]),
    //                         vec4(geometry_data[10], geometry_data[11], geometry_data[12], geometry_data[13]),
    //                         vec4(geometry_data[14], geometry_data[15], geometry_data[16], geometry_data[17]) );
    //     vec4 pos_transformed =  transpose(matrix) * vec4(p , 1.);

    //     float dmin = 9999999.;
    //     int coords_num = int(geometry_data[18]);
    //     int points_num = int(coords_num/3);
    //     vec3 [points_num] up; 
    //     vec3 [points_num] points; 
    //     for (int i = 0; i < points_num; i++){
    //         up[i] = abs((pos_transformed % unitcell) - unitcell/2.);
    //     }        
    //     for (int i = 0; i < points_num; i += 3){
    //         points[i/3] = vec3(geometry_data[18+i], geometry_data[18+i+1], geometry_data[18+i+2]);
    //     }
    //     int pos = int(18 + coords_num + 1);
    //     int types_num = geometry_data[pos];
    //     for (int i = 0; i < types_num; i += 2){
    //         vec2 l = vec2(geometry_data[pos+i], geometry_data[pos +i + 1]);
    //     }
    // }
    // return 1.
// }










