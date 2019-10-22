#version 120

#ifdef GL_ES
precision mediump float;
#endif

#define object_max_num    30 // CAREFUL, MEMORY LIMITED
#define geom_data_max_num 200
#define max_num_of_children 30

#define resolution_of_texture 1024

///---------------------------------------------------------------- INPUTS
uniform vec2 u_resolution;
uniform vec3 camera_POS;
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

float VolPrimitive(in vec3 p, in int id, in int current_index, in float[20] geometry_data){ //current_index only needed for 
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

float VolCombination(in int id, in float[max_num_of_children] geometry_data, in int count){
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

float VolModification(in int id, in int index, in float [20] data){
    // Shell
    if (id == Shell_id){ //// The shell theoretically needs to know the child. But practically it's always the next index 
        float current_dist = objects_values[index+1]; 
        float d = data[0];
        float s = data[1];
        return abs(current_dist + (s - 0.5) * d) - d/2.0;
    } else {
        return 0.;
    }
}

///// MICROSTRUCTURES
#define Lattice_id 400
// float VolMicrostructure(in vec3 p, in int id, in int index, in float [100] geometry_data){
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

///// -------------------- Get distance 

float dist_final;
float dist;
int current_index;
int current_id;
int parent_index; 
int parent_id;
int count;


float y_slicing_Plane(vec3 p, float y_of_plane){
    return -(p.y - y_of_plane);
}

float GetDistance(vec3 p){ //union of shapes  
    int pos = 0;
    for (int i = 0; i < object_max_num -1; i++ ){ 
    //     //---- get data
        current_index = int(v_indices[i]);
        current_id = int(v_ids[i]);
        count = int(v_data_count_per_object[i]);

        float [20] geometry_data ;
        for (int j=0 ; j < v_data_count_per_object[i]; j++){
            geometry_data[j] = v_object_geometries_data[pos + j];
        }

        /////------ Get dist of current object
        //primitive
        if (current_id == VolSphere_id || current_id == VolBox_id || current_id == VolTorus_id || current_id == VolCylinder_id){
            dist = VolPrimitive(p, current_id, current_index, geometry_data);
            objects_values[current_index] = dist;
        //combination
        } else if (current_id == Union_id || current_id ==  Intersection_id ||current_id ==  Smooth_Union_id ){
            dist = VolCombination(current_id, geometry_data, count); /// HERE!!!
            objects_values[current_index] = dist;
        //modification
        } else if(current_id == Shell_id){ // Shell FIX HERE: UNIVERSAL MODIFICATION
            dist = VolModification(current_id , current_index, geometry_data);
            objects_values[current_index] = dist;  
        }
        pos += int(v_data_count_per_object[i]);

        /////----- break loop once the necessary values have been calculated
        if (current_index ==  display_target_object || current_index == 1 ){ //display_target_object
            dist_final = objects_values[display_target_object];

            // intersect wih slicing plane !!!!!!!!!!!!!!!HERE THIS SHOULD HAPPEN ONLY IF SLICING PLANE EXISTS
            float y_slice_plane_dist = y_slicing_Plane(p, y_slice);
            return max(dist_final, y_slice_plane_dist);

            return dist_final;
        }
    }  
}


///// --------------------Raymarching
int total_steps = 0;

#define MAX_STEPS 200
#define MAX_DIST 200.
#define SURF_DIST 0.02
float RayMarch(vec3 ro, vec3 rd){ // ray origin, ray direction
    float dO = 0.; // distance from origin

    for (int i = 0;  i< MAX_STEPS; i++){
        vec3 p = ro + rd * dO;
        float dS = GetDistance(p); // Get distance scene
        dO += dS;
        total_steps += 1;
        if (dO> MAX_DIST || dS < SURF_DIST) break;
    }
    return dO;
}


///// --------------------Visualization functions

vec3 GetNormal(vec3 p){
    float d = GetDistance(p);
    //evaluate distance of points around p
    vec2 e = vec2(.01 , 0); // very small vector
    vec3 n = d - vec3(GetDistance(p-e.xyy), // e.xyy = vec3(.01,0,0)
                      GetDistance(p-e.yxy),
                      GetDistance(p-e.yyx));
    return normalize(n);
}

float GetLight (vec3 p){ //gets the position of intersection of ray with shape
    vec3 LightPos = vec3(0 , 5, 6);
    // LightPos.xz += vec2( sin(u_time) , cos(u_time));

    vec3 l = normalize(LightPos - p); // vector from light source to position
    vec3 n = GetNormal(p);
    float dif = clamp(dot(n, l)  , 0., 1.);

    //compute shadows
    float d = RayMarch(p+n * SURF_DIST,l);
    if(d<length(LightPos -p)){
        dif *= .3;
    }
    return dif;
}


// ---- extra inputs for post-processing
// buffers
uniform sampler2D color_texture;
uniform sampler2D depth_buffer;
// transformationm matrix of perspective camera (can't use matrices of default orthographic camera)
uniform mat4 transform_clip_plane_to_perspective_camera;

vec3 findRayDirection(in vec2 uv){
    vec4 pixel_world_coords =  transform_clip_plane_to_perspective_camera * vec4(uv.x, uv.y, 1., 1.);
    vec3 rd = pixel_world_coords.xyz;
    return normalize(rd);
}

///---------------------------------------------------------------- DEPTH  
vec3 World_position_from_depth(in float depth, in vec2 uv){
    vec2 st_ = uv * 2.0 - 1.0;          //translate 0s at the center of the image, range [-1,1]
    depth =  depth * 2.0 - 1.0;   //do the same for depth values 
    vec4 clipSpacePosition =  vec4(st_.x, st_.y, depth, 1.);
    vec4 viewSpacePosition = transform_clip_plane_to_perspective_camera * clipSpacePosition;
    viewSpacePosition /= viewSpacePosition.w; // Perspective division
    return viewSpacePosition.xyz;
    }


void main()
{
    vec2 st = gl_FragCoord.xy / u_resolution.xy;
    vec2 texture_uv = gl_FragCoord.xy / vec2(resolution_of_texture);

    // ------------- get information from buffers
    vec4 color_pixel = texture2D(color_texture, texture_uv.xy);  
    vec4 depth_pixel = texture2D(depth_buffer, texture_uv.xy); 

    // ------------- calculate distance of objects
    vec3 world_pos_object = World_position_from_depth(depth_pixel.x, st.xy);
    float dist_object = length(world_pos_object - camera_POS); //distance of rendered objects from camera 

    // ------------- ray marching 
    vec2 uv = 2*(st - vec2(0.5, 0.5)); //put 0 in the center of the window, range of values: [-1,1]
    vec3 ro = camera_POS.xyz; // ray origin : camera position (world coordinates)
    vec3 rd = findRayDirection(uv);
    float d = RayMarch(ro, rd);
    vec3 world_pos_SDF = ro + rd * d; // position of intersection of ray with solid

    float dist_SDF = length(world_pos_SDF - camera_POS); //distance of SDF in current position from camera 
    vec3 color_of_SDF = vec3(GetNormal(world_pos_SDF) * -1.);

    // check depth and color accordingly
    vec3 color = vec3(0.);
    if (dist_object > dist_SDF && dist_SDF < 200){
       
        if (abs(world_pos_SDF.y - y_slice) < 0.1) {
            color = vec3(0.1, 0.1, 0.1);  // color white section
        } else {
            color = color_of_SDF ; }
    } else {
        color = color_pixel.xyz;
    }

    // color = vec3( total_steps / 50. ); // display number of steps 
    gl_FragColor = vec4(color, 1.);
}
