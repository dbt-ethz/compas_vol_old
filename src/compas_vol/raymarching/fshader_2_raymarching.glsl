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
            dist = VolCombination(current_id, geometry_data, count);
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

// float GetSunLight (vec3 p, vec3 normal){ //gets the position of intersection of ray with shape
//     vec3 LightPos = vec3(5 , -5, 16);
//     vec3 l = normalize(LightPos  - p); // vector from light source to position
//     return clamp(dot(normal, l)  , 0., 1.);
//     // //compute shadows
//     // float d = RayMarch(p+n * SURF_DIST,l);
//     // if(d<length(LightPos -p)){
//     //     dif *= .3;
//     // }
// }

// float GetSkyLight (vec3 p, vec3 normal){
//     vec3 sunPos = vec3(0.,10.,0.);
//     return clamp(dot(normal, sunPos), 0., 1.);
// }