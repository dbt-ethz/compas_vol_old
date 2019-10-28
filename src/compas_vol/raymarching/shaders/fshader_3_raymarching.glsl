///// -------------------- Get distance 
float dist_final;
float dist;
int current_index;
int current_id;
int parent_index; 
int parent_id;
int count;

float GetDistance(vec3 p){ //union of shapes  

    int pos = 0;
    float bounding_sphere_distance = bounding_sphere_primitive(p, bounding_sphere.xyz, bounding_sphere.w);
    float dist_final = abs(bounding_sphere_distance) + 1. ; // HERE THIS NEEDS ATTENTION, shouldn't be too big
    if (bounding_sphere_distance < 0) { // if withing the bounding sphere. OPTIMIZATION. // HERE THIS NEEDS ATTENTION, how to find dimensions of bounding sphere
    
        for (int i = 0; i < object_max_num -1; i++ ){ 
            //---- get data
            current_index = int(v_indices[i]);
            current_id = int(v_ids[i]);
            count = int(v_data_count_per_object[i]);

            float [max_num_of_geom_data] geometry_data ;
            for (int j=0 ; j < v_data_count_per_object[i]; j++){
                geometry_data[j] = v_object_geometries_data[pos + j];
            }


            /////------ Get dist of current object
            //primitive
            if (current_id == VolSphere_id || current_id == VolBox_id || current_id == VolTorus_id || current_id == VolCylinder_id){
                dist = VolPrimitive(p, current_id, current_index, geometry_data);
                objects_values[current_index] = dist;
            //combination
            } else if (current_id == Union_id || current_id ==  Intersection_id || current_id ==  Smooth_Union_id || current_id ==  Subtraction_id){
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
                break;
            }
        }
        dist_final = segmentation_offset(dist_final, 0.02);
        // dist_final = segmentation_plane_z(p, dist_final, 0.025, 200, -5.);



        // intersect with slicing planes 
        dist_final =  max(dist_final, y_slicing_Plane(p, y_slice));
        dist_final =  max(dist_final, z_slicing_Plane(p, z_slice));

        // dist_final = ripples_sin(p, dist_final, 0.02, 50 ); //float amplitude, float frequency
        // dist_final = ripples_fract(p, dist_final, 0.02, 20 ); //float amplitude, float frequency                 
    }  
    
    // dist_final = ripples_sin(p, dist_final, 0.02, 30 ); //float amplitude, float frequency
    return dist_final;
}


///// --------------------Raymarching
int total_steps = 0;

#define MAX_STEPS 100
#define MAX_DIST 100.
#define SURF_DIST 0.001
float RayMarch(vec3 ro, vec3 rd){ // ray origin, ray direction
    float t = 0.; // distance from origin

    for (int i = 0;  i< MAX_STEPS; i++){

        vec3 p = ro + rd * t;
        float distance_sdf = GetDistance(p); // Get distance scene

        // if (0< distance_sdf && distance_sdf< 1.){
        //     t += distance_sdf * 0.03;
        // }else {

        if (distance_sdf < SURF_DIST){
            distance_sdf = 0.;
        }
        
        // if (0 < distance_sdf && distance_sdf< 1.){
        //     t +=  distance_sdf *0.1;
        // } else{
        //     t += distance_sdf;    
        // }

        t += distance_sdf;    
        total_steps += 1;

        if (t> MAX_DIST || abs(distance_sdf) < SURF_DIST) break;
    }
    return t;
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

// float GetLight_point (vec3 p){ //gets the position of intersection of ray with shape
//     vec3 LightPos = vec3(0 , 5, 6);
//     // LightPos.xz += vec2( sin(u_time) , cos(u_time));

//     vec3 l = normalize(LightPos - p); // vector from light source to position
//     vec3 n = GetNormal(p);
//     float dif = clamp(dot(n, l)  , 0., 1.);

//     //compute shadows
//     float d = RayMarch(p+n * SURF_DIST,l);
//     if(d < length(LightPos -p)){
//         dif *= .3;
//     }
//     return dif;
// }

float CalculateOcclusion( in vec3 pos, in vec3 normal){
	float occ = 0.0;
    float sca = 1.0;
    for( int i=0; i<5; i++ )
    {
        float h = SURF_DIST + 0.03 * float(i)/4.0;
        vec3 opos = pos + h * normal;
        float d = GetDistance(opos);
        occ += (h-d)*sca;
        sca *= 0.95;
    }
    return clamp( 1.0 - 3.0*occ, 0.0, 1.0 );
}

#define sun_shadow_dist 100; 
vec3 GetLight(in vec3 normal, in vec3 pos){
    vec3 sun_color        = vec3(7.0, 5.0, 3.0); //normalize?? Looks too dull...
    vec3 sky_color        = vec3(0.5, 0.8, 0.95);
    vec3 bounce_color     = vec3(0.7, 0.3, 0.2);

    vec3 sun_direction    = normalize(vec3(5, -3, 6));
    vec3 sky_direction    = vec3(0.0, 0.0, 1.0);
    vec3 bounce_direction = vec3(0.0, 0.0, -1.0);

    float sun_dif    = clamp(dot(normal, sun_direction), 0.0, 1.0);
    float sky_dif    = clamp(0.6 + 0.5 * dot(normal, sky_direction), 0.0, 1.0);
    float bounce_dif = clamp(0.6 + 0.5 * dot(normal, bounce_direction), 0.0, 1.0);

    // float sun_shadow = step( RayMarch(pos + normal * (SURF_DIST + 0.01) , -sun_direction), 0);
    
    float sun_shadow = 1.;
    float len_sun_shadow = RayMarch(pos + normal * (SURF_DIST + 0.01) , sun_direction);
    if(len_sun_shadow < MAX_DIST ){
        sun_shadow *= .3;
    }

    // float occlusion = CalculateOcclusion(pos, normal);
    // return vec3(occlusion * occlusion); // if use occlusion, multiply it with all returned colors 


    return sun_color * sun_dif * sun_shadow + 
           sky_color * sky_dif + 
           bounce_color * bounce_dif ;
}































