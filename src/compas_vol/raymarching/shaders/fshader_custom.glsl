#version 120
///// This is coming from a (wonderful and 6 hrs long!) live shader deconstruction by Inigo Quilez
///// https://www.youtube.com/watch?v=Cfe5UQ-1L9Q
///// 3h 03 min

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

float sdStick(in vec3 pos, vec3 a, vec3 b, float ra, float rb){
    vec3 ba = b-a;
    vec3 pa = pos-a;
    float h = clamp( dot(pa,ba) / dot(ba,ba), 0.0, 1.0);
    float radius = mix(ra, rb, h);
    return length(pa - h * ba) - radius;
}

vec2 sdCharacter(in vec3 pos){ // returns distance and object id

    float int_time = floor(osg_FrameTime);
    float fract_time = fract(osg_FrameTime);

    float time = fract(osg_FrameTime);
    float dy = 4.0 * (1.0 - fract_time) * fract_time; // parabola (time) for vertical movement
    // float fract_time = 0.5; 


    //body
    float dz = int_time +fract_time;  //pow(fract_time, 0.1);
    float dx =  -1 + 2.0 * abs(fract(osg_FrameTime * 0.5)  - 0.5) / 0.5;
    vec3 cen = vec3(dx * 0.8 , 0.25+dy , 0.+dz);
    float r_scale_y = 0.5 + 0.5* dy;
    float r_scale_z = 1/r_scale_y;
    vec3 r = vec3(0.25, 0.25 * r_scale_y, 0.25 * r_scale_z); //radius of elipsoid

    vec3 body_position = pos - cen;
    

    // animation trick that doesnt work very well
    // float derivative_of_parabola = 1/4.0 *(1.0 - 2.0*time); // tangent of parabola
    // float rc = cos(derivative_of_parabola);
    // float rs = sin(derivative_of_parabola);    
    // body_position.xy = mat2(rc,rs,-rs,rc)*body_position.xy;       
    // vec2 uu = normalize(vec2(1., derivative_of_parabola)); //parallel to tangent
    // vec2 vv = normalize(vec2(-derivative_of_parabola, 1.0)); //perpendicular to u
    // body_position.yz = vec2( dot(uu,body_position.yz), dot(vv,body_position.yz));  //multiplications for the squeezing

    vec3 body_position_symmetric = vec3 (abs(body_position.x), body_position.y, body_position.z);

    float body = sdElipsoid(body_position, r);

    

    //head 
    float head         = sdElipsoid(body_position - vec3(0.,0.3,0.), vec3(0.15, 0.2, 0.23));
    float back_of_head = sdElipsoid(body_position - vec3(0.,0.3,-0.08), vec3(0.23, 0.2, 0.2));
    float body_head_dist = smooth_union(body, smooth_union(head, back_of_head, 0.05), 0.1);

    //eyebrows
    // vec3 eb = body_position_symmetric - vec3(0.13,0.4,0.14);
    // eb.xy = (mat2(8., 15., -15., 15.)/17.) * eb.xy; //rotation of the vector.xy using a pythagorean triplet 
    // float eyebrows_dist = sdElipsoid(eb , vec3(0.06, 0.035,0.04));
    // body_head_dist = smooth_union(body_head_dist, eyebrows_dist, 0.06);

    //mouth
    float dy_for_smiling = 5.0*body_position.x*body_position.x; // parabola
    float mouth_dist = sdElipsoid(body_position -vec3(0.0, 0.18 + dy_for_smiling, 0.1), vec3(0.1, 0.035, 0.16));
    body_head_dist = smooth_subtraction(body_head_dist, -mouth_dist, 0.04);

    //wrinkles 
    float wrinkles_y = body_position.y- 2.5* body_position.x*body_position.x; //along they y-height, minus parabola for curve
    body_head_dist += 0.002 * sin(wrinkles_y * 160.0) * (1 - smoothstep(0.0, 0.15, abs(wrinkles_y)));

    //ears
    float ears_dist = sdStick(body_position_symmetric, vec3(0.1,0.3,0.0), vec3(0.2,0.6,0.0), 0.005, 0.02);
    body_head_dist = smooth_union(body_head_dist, ears_dist, 0.04);

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

float GetGroundPattern(in vec3 pos){
    float tile =18.0;
    float f = -1 + 2 * smoothstep (-0.2, 0.2, sin(tile * pos.x) +sin(tile * pos.y) + sin(tile * pos.z)); //sinwaves instead of perlin noise for better performance
    return 0.2 * f; //PATTERN! is added to color and shape as displacement
}

vec2 GetDistance(in vec3 pos) // GetDistance : my GetDistance function 
{
    vec2 character_return_vec = sdCharacter(pos);
    float character_distance = character_return_vec.x;

    // ground 
    float plane_pos_y = 0.05 + 0.08* sin(2.0*pos.x) + 0.1* sin(2.0*pos.z);
    float floor_distance = pos.y - plane_pos_y; 

    vec3 pos_repeated = vec3(mod(abs(pos.x) , 3.), pos.y, mod(pos.z, 3.0) -1.4 ); // REPETITION OF ELEMENTS, mod, fract
    vec2 hill_id = vec2(floor(abs(pos.x)/3.), floor(pos.z/3.0)); // unique identifier per hill based on position
    float floating_point_id = hill_id.x * 131.1 + hill_id.y * 371.7; // multiplication with random numbers

    vec3 radius =  vec3(0.7, 1.2 * sin(floating_point_id), 0.7);
    radius -= 0.1 *(sin(pos.y*3.) + sin(pos.z) ); //sin(pos.x*3.) +
    float hills = sdElipsoid(pos_repeated - vec3( 2.0, 0., 0.), radius);
    hills -= 0.025 * GetGroundPattern(pos);  //PATTERN, same as in coloring
    floor_distance = smooth_union(floor_distance, hills , 0.3);

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
        vec3 pos = ro + t * rd;
        vec2 distance_return_vector = GetDistance(pos);
        float h = distance_return_vector.x;
        id = distance_return_vector.y;
        if (abs(h) < 0.001) break;
        t += h;
        if (t > max_dist) break;//far clipping plane   
    }
    if (t > max_dist) t = -1;
    return vec2(t, id);
}

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

    // float rotation_time = osg_FrameTime * 0.5 ;
    float rotation_time = 3.14;
    
    // camera 
    float cam_dist = 5.0;
    vec3 ro = vec3(0., 0.7, cam_dist + osg_FrameTime);
    // vec3 ro = vec3(cam_dist * sin(rotation_time), 0.7, + cam_dist * cos(rotation_time) +  osg_FrameTime ); // ray origin

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

        if (id == floor_id){ //attention when comparing floats
            object_material = vec3(0.05, 0.1 ,0.02); //this material will be textured
            // float tile =18.0;
            // float f = -1 + 2 * smoothstep (-0.2, 0.2, sin(tile * pos_of_hit.x) +sin(tile * pos_of_hit.y) + sin(tile * pos_of_hit.z)); //sinwaves instead of perlin noise for better performance
            object_material += GetGroundPattern(pos_of_hit)* vec3(0.06, 0.06, 0.02);  //0.2 * f * vec3(0.06, 0.06, 0.02); //PATTERN! is added to the shape itself also as displacement
        } 

        if (id == skin_id)    { object_material = vec3(0.2); }
        if (id == eyes_id)    { object_material = vec3(0.4, 0.4, 0.4); }
        if (id == pupils_id)  { object_material = vec3(0.1, 0.1, 0.4); }
         
        color = object_material * GetLight(normal, pos_of_hit);
    }

    color = pow( color, vec3(0.4545)); // square root. Gamma correction

    // color = vec3(t/40);
    gl_FragColor = vec4(color , 1.);

}