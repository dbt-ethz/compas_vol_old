#version 120
///// This is coming from a (wonderful and 6 hrs long!) live shader deconstruction by Inigo Quilez
///// https://www.youtube.com/watch?v=Cfe5UQ-1L9Q

uniform vec2 u_resolution;
uniform float osg_FrameTime;

const float floor_id  = 1.0;
const float skin_id   = 2.0;
const float eyes_id   = 3.0;
const float pupils_id = 4.0;


float smooth_union(in float a, in float b, float k){
    float h = max(k - abs(a-b), 0.0);
    return min(a,b) - h*h/(k*4.0);
}

float smooth_subtraction(in float a, in float b, float k){
    float h = max(k - abs(a-b), 0.0);
    return max(a,b) + h*h/(k*4.0);
}

float sdSphere(in vec3 pos, in float r){
    return length(pos)-r;
}

float sdElipsoid(in vec3 pos, in vec3 r){
    float k0 = length(pos/r);
    float k1 = length(pos/r/r); 
    return k0 * (k0 - 1.0)/k1;
}



vec2 sdCharacter(in vec3 pos){ // returns distance and object id
    float time = 0.5; 
    // float time = fract(osg_FrameTime);
    float y = 4.0 * (1.0 - time) * time; // parabola (time) for vertical movement

    //body
    vec3 cen = vec3(0,0.25 + y,0);
    float r_scale_y = 0.5 + 0.5*y;
    float r_scale_z = 1/r_scale_y;
    vec3 r = vec3(0.25, 0.25 * r_scale_y, 0.25 * r_scale_z); //radius of elipsoid

    vec3 body_position = pos - cen;
    float derivative_of_parabola = 4.0 *(1.0 - 2.0*time); // tangent of parabola
    vec2 u = normalize(vec2(1., derivative_of_parabola)); //parallel to tangent
    vec2 v = normalize(vec2(-derivative_of_parabola, 1.0)); //perpendicular to u
    body_position.yz = vec2(dot(u, body_position.yz), dot(v, body_position.yz)); //multiplications for the squeezing 
    float body = sdElipsoid(body_position, r);

    //head 
    float head         = sdElipsoid(body_position - vec3(0.,0.3,0.), vec3(0.15, 0.2, 0.23));
    float back_of_head = sdElipsoid(body_position - vec3(0.,0.3,-0.08), vec3(0.23, 0.2, 0.2));
    float body_head_dist = smooth_union(body, smooth_union(head, back_of_head, 0.05), 0.1);

    vec3 body_position_symmetric = vec3 (abs(body_position.x), body_position.y, body_position.z);
    
    //eyebrows
    vec3 eb = body_position_symmetric - vec3(0.13,0.4,0.14);
    eb.xy = (mat2(8., 15., -15., 15.)/17.) * eb.xy; //rotation of the vector.xy using a pythagorean triplet 

    float eyebrows_dist = sdElipsoid(eb , vec3(0.06, 0.035,0.04));
    body_head_dist = smooth_union(body_head_dist, eyebrows_dist, 0.06);

    //mouth
    float mouth_dist = sdElipsoid(body_position -vec3(0.0, 0.18, 0.1), vec3(0.08, 0.035, 0.3));
    body_head_dist = smooth_subtraction(body_head_dist, -mouth_dist, 0.04);

    //eyes
    float eyes_dist   = sdSphere(body_position_symmetric - vec3(0.1, 0.3, 0.15), 0.05);
    float pupils_dist = sdSphere(body_position_symmetric - vec3(0.11, 0.3, 0.2), 0.013);

    // float character_dist = min(body_head_dist, min(eyes_dist, pupils_dist)); 

    vec2 return_vec = vec2(body_head_dist, skin_id);
    if (eyes_dist < min(body_head_dist, pupils_dist)) {
        return_vec = vec2(eyes_dist, eyes_id);
    } if (pupils_dist < min(body_head_dist, eyes_dist)){
        return_vec = vec2(pupils_dist, pupils_id);
    }

    return  return_vec;
}

vec2 GetDistance(in vec3 pos) // GetDistance : my GetDistance function 
{
    vec2 character_return_vec = sdCharacter(pos);
    float character_distance = character_return_vec.x;

    // ground 
    float plane_pos_y = 0.1;
    float floor_distance = pos.y - plane_pos_y; 


    // return min(character_distance, floor_distance);
    // return character_return_vec;
    return (floor_distance < character_distance) ? vec2(floor_distance, floor_id) : character_return_vec;
}


vec3 GetNormal(in vec3 pos){
    vec3 e = vec3(0.01, 0. ,0.);
    return normalize( vec3(GetDistance(pos + e.xyy).x - GetDistance(pos - e.xyy).x,
                           GetDistance(pos + e.yxy).x - GetDistance(pos - e.yxy).x,
                           GetDistance(pos + e.yyx).x - GetDistance(pos - e.yyx).x )); 
                           // .x to get the distance value, .y to get the id
}


#define max_dist 30.0 
#define max_step 100.0 
vec2 RayMarch(in vec3 ro, in vec3 rd){  
    float id = -1.0;  
    float t = 0.0;
    for (int i = 0; i<max_step; i++)
    {
        vec3 pos = ro + t*rd;
        vec2 distance_return_vector = GetDistance(pos);
        float h = distance_return_vector.x;
        id = distance_return_vector.y;
        if (h < 0.01) break;
        t += h;
        if (t > max_dist) break;//far clipping plane   
    }
    if (t > max_dist) t = -1;
    return vec2(t, id);
}

// float CastShadow(in vec3 ro, vec3 rd){// similar to ray marching, but we are also recording proximity
//     float result = 1.0;
//     float t = 0.01;
//     for (int i=0; i < max_step; i++){
//         vec3 pos = ro + t*rd; 
//         float h = GetDistance(pos).x;
//         result = min(result, (16.0 * h/t) );
//         t+= h;
//         if (result < 0.01) break;
//         t += h;
//         if (t > max_dist) break;//far clipping plane   
//     }
//     return result;
// }

vec3 GetLight(in vec3 normal, in vec3 pos_of_hit){
    vec3 sun_color        = vec3(7.0, 5.0, 3.0);
    vec3 sky_color        = vec3(0.5, 0.8, 0.95);
    vec3 bounce_color     = vec3(0.7, 0.3, 0.2);

    vec3 sun_direction    = normalize(vec3(0.8, 0.4, 0.3));
    vec3 sky_direction    = vec3(0.0, 1.0, 0.0);
    vec3 bounce_direction = vec3(0.0, -1.0, 0.0);

    float sun_dif    = clamp(dot(normal, sun_direction), 0.0, 1.0);
    float sky_dif    = clamp(0.6 + 0.5 * dot(normal, sky_direction), 0.0, 1.0);
    float bounce_dif = clamp(0.6 + 0.5 * dot(normal, bounce_direction), 0.0, 1.0);

    float sun_shadow = step( RayMarch(pos_of_hit + normal* 0.01 , sun_direction).x, 0.0) ;
    // float sun_shadow = CastShadow(pos_of_hit + normal* 0.01 , sun_direction);
    return sun_color * sun_dif * sun_shadow + sky_color * sky_dif + bounce_color * bounce_dif;
}

void main(){  
    vec2 p = gl_FragCoord.xy / u_resolution.xy;
    p = 2*(p - vec2(0.5, 0.5)); // normalize (put on the center of the screen) 

    float time = osg_FrameTime * 0.5;
    // time = 3.14;
    
    // camera 
    float cam_dist = 5.0;
    vec3 ro = vec3(cam_dist * sin(time), 0.7, - cam_dist * cos(time)); // ray origin

    vec3 ta = vec3(0.0, 1.0, 0.0); //target point

    vec3 ww = normalize(ta - ro); 
    vec3 uu = normalize(cross(ww, vec3(0., 1., 0.)));
    vec3 vv = normalize(cross(uu, ww));

    vec3 rd = normalize(p.x * uu + p.y * vv + 2.5* ww );  //ray direction. Near plane: 2.5 field of view

    // background sky color
    vec3 color = vec3(0.5, 0.75, 0.87) - 0.45 * rd.y; //blue that becomes brighter as the y decreases
    color = mix(color, vec3(0.7, 0.75, 0.8), exp(-20* rd.y));

    vec2 result_vector_of_raymarch = RayMarch(ro, rd);
    float t  = result_vector_of_raymarch.x; // distance
    float id = result_vector_of_raymarch.y; // material

    if (t > 0){ //if we have hit something
        vec3 pos_of_hit = ro + t*rd; 
        vec3 normal = GetNormal(pos_of_hit);

        vec3 object_material = vec3(0.18); // default material albedo

        if (id == floor_id)   { object_material = vec3(0.05, 0.1 ,0.02); } //attention when comparing floats
        if (id == skin_id)    { object_material = vec3(0.2); }
        if (id == eyes_id)    { object_material = vec3(0.4, 0.4, 0.4); }
        if (id == pupils_id)  { object_material = vec3(0.1, 0.1, 0.4); }
         
        color = object_material * GetLight(normal, pos_of_hit);
    }

    color = pow( color, vec3(0.4545)); // square root. Gamma correction

 
    gl_FragColor = vec4(color , 1.);

}