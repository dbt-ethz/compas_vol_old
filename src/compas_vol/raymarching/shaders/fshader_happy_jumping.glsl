#version 120
///// This shader code is coming from a (wonderful and 6 hrs long!) live shader deconstruction by Inigo Quilez
///// https://www.youtube.com/watch?v=Cfe5UQ-1L9Q
///// https://www.shadertoy.com/view/3lsSzf

uniform vec2 u_resolution;
uniform float osg_FrameTime;

const float floor_id  = 1.0;
const float skin_id   = 2.0;
const float eyes_id   = 3.0;
const float pupils_id = 4.0;
const float candy_id  = 5.0;


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
    vec2 return_vec = vec2(2., skin_id); //initialize on default values 

    float int_time = floor(osg_FrameTime);
    float fract_time = fract(osg_FrameTime);

    float time = fract(osg_FrameTime);
    float dy = 6.0 * (1.0 - fract_time) * fract_time; // parabola (time) for vertical movement


    //body
    float dz = int_time +fract_time;  //pow(fract_time, 0.1);
    float dx =  -1 + 2.0 * abs(fract(osg_FrameTime * 0.5)  - 0.5) / 0.5;
    vec3 cen = vec3(dx * 0.6 , 0.25+dy , 0.+dz);
    float r_scale_y = 0.5 + 0.5* dy;
    float r_scale_z = 1/r_scale_y;
    vec3 r = vec3(0.25, 0.25 * r_scale_y, 0.25 * r_scale_z); //radius of elipsoid

    vec3 body_position = pos - cen;

    float rotation = dx* 0.35;
    body_position.xy = mat2( cos(rotation), -sin(rotation), sin(rotation), cos(rotation) ) * body_position.xy ;
    vec3 body_position_symmetric = vec3 (abs(body_position.x), body_position.y, body_position.z);
    float body = sdElipsoid(body_position, r);

    //bounding volume around entire body. OPTIMIZATION. Only compute body if within bounding volume.
    if (body< 2.0) {
        //head 
        float head_animation = -1 + 2* smoothstep(-0.3, 0.3, sin(osg_FrameTime));
        head_animation *= 0.75;
        mat2 head_rotation_matrix = mat2(cos(head_animation), sin(head_animation), -sin(head_animation), cos(head_animation));
        vec3 head_pos =  vec3(0.,0.3,0.);
        vec3 bp_head = body_position;
        bp_head.xz = head_rotation_matrix * bp_head.xz;

        vec3 bp_head_symmetric = vec3 (abs(bp_head.x), bp_head.y, bp_head.z);

        float head         = sdElipsoid(bp_head - head_pos, vec3(0.15, 0.2, 0.23));
        float back_of_head = sdElipsoid(bp_head - head_pos - vec3(0.,0.,-0.08), vec3(0.23, 0.2, 0.2));
        float body_head_dist = smooth_union(body, smooth_union(head, back_of_head, 0.05), 0.1);

        //mouth
        float dy_for_smiling = 5.0*bp_head.x*bp_head.x; // parabola
        float mouth_dist = sdElipsoid(bp_head -vec3(0.0, 0.18 + dy_for_smiling, 0.1), vec3(0.1, 0.035, 0.16));
        body_head_dist = smooth_subtraction(body_head_dist, -mouth_dist, 0.04);

        //wrinkles 
        float wrinkles_y = body_position.y- 2.5* body_position.x*body_position.x; //along they y-height, minus parabola for curve
        body_head_dist += 0.002 * sin(wrinkles_y * 100.0) * (1 - smoothstep(0.0, 0.15, abs(wrinkles_y)));

        //arms 
        float hr = sin(0.791*osg_FrameTime);
        hr = 0.7*sign(hr)*smoothstep(0.5,0.7,abs(hr));
        float p2 = 0.5-0.5*cos(6.2831*fract_time);
        float arms = sdStick(body_position_symmetric, vec3(0.18-0.06*hr*sign(r.x),0.2,-0.05), vec3(0.3+0.1*p2,+0.+ 0.3*p2,-0.15), 0.03, 0.06  );
        body_head_dist = smooth_union(body_head_dist, arms, 0.01+0.04*(1.0-body_position.y)*(1.0-body_position.y)*(1.0-body_position.y)  ); //cubic change of smoothing factor for the arms

        //legs
        float legs_animation_time =cos(osg_FrameTime * 3.14);
        float legs_dy = -cos(legs_animation_time);
        float legs_dz = sin(legs_animation_time);
        vec3 base_of_legs = vec3(0.1, -0.15, 0.0); 
        float legs = sdStick(body_position_symmetric, base_of_legs, base_of_legs + vec3(0.07, -0.1, -0.5 + legs_dz * sign(body_position.x)), 0.06, 0.08  );
        body_head_dist = smooth_union(body_head_dist, legs, 0.04);

        //ears
        float ears_dist = sdStick(bp_head_symmetric, vec3(0.1,0.3,0.0), vec3(0.2,0.6,0.0), 0.005, 0.02);
        body_head_dist = smooth_union(body_head_dist, ears_dist, 0.04);

        //eyes
        vec3 eyes_pos = vec3(0.1, 0.3, 0.14);
        float eyes_dist   = sdSphere(bp_head_symmetric - eyes_pos, 0.05);
        float pupils_dist = sdSphere(bp_head_symmetric - vec3(0.11, 0.3, 0.18), 0.013);

        //eyebrows
        // float dx_eyebrow = 0.13 ;
        // float dy_for_smiling_eyebrows = 2.0* bp_head.x * bp_head.x; // parabola
        // vec3 eb = bp_head_symmetric - vec3(0.13,0.4 -dy_for_smiling_eyebrows ,0.15);
        // // eb.xy = (mat2(8., 15., -15., 15.)/17.) * eb.xy; //rotation of the vector.xy using a pythagorean triplet 
        // float eyebrows_dist = sdElipsoid(eb , vec3(0.06, 0.075,0.03));
        // body_head_dist = smooth_union(body_head_dist, eyebrows_dist, 0.04);

        return_vec = vec2(body_head_dist, skin_id);
        if (eyes_dist < min(body_head_dist, pupils_dist)) {
            return_vec = vec2(eyes_dist, eyes_id);
        } if (pupils_dist < min(body_head_dist, eyes_dist)){
            return_vec = vec2(pupils_dist, pupils_id);
        }
    }
    else{ //then skip calculating the character
        return_vec = vec2(body, skin_id);
    }
    return  return_vec;
}

float GetGroundPattern(in vec3 pos){
    float tile =18.0;
    float f = -1 + 2 * smoothstep (-0.2, 0.2, sin(tile * pos.x) +sin(tile * pos.y) + sin(tile * pos.z)); //sinwaves instead of perlin noise for better performance
    return 0.2 * f; //PATTERN! is added to color AND shape (as displacement)
}

vec2 sdLandscape(in vec3 pos){
    // ground 
    float plane_pos_y = 0.05 + 0.08* sin(2.0*pos.x - 1.2) + 0.1* sin(2.0*pos.z);
    float floor_distance = pos.y - plane_pos_y;  
    float spacing = 4.;
    vec3 pos_repeated = vec3(mod(abs(pos.x) , spacing), pos.y, mod(pos.z, spacing) -spacing*0.5 ); // REPETITION OF ELEMENTS, mod, fract
    vec2 hill_id = vec2(floor(pos.x/spacing), floor(pos.z/spacing)); // unique identifier per hill based on position
    float floating_point_id = hill_id.x * 11.231 + hill_id.y * 71.457; // multiplication with random big numbers
    vec3 radius =  vec3(0.9, 1.3 , 1.0); //* sin(floating_point_id * 245.24 * sign(pos.x))

    // hills animation
    float hills_frequency = 0.2;
    float y_max_hills = 6.;
    float y_min_hills = -2.;
    float dy_hills = y_min_hills + fract( osg_FrameTime * hills_frequency +  floating_point_id) * y_max_hills;     //0.1*exp(-k*k)*sin(tt)*exp(-max(tt,0.0)/2.0)*smoothstep(0.0,0.01,t5);
    float hills = sdElipsoid(pos_repeated - vec3( 2.0, dy_hills, 0.), radius* ( 1  - (dy_hills - y_min_hills)/y_max_hills * (dy_hills - y_min_hills)/y_max_hills ));
    hills -= 0.035 * GetGroundPattern(pos);  //PATTERN, same as in coloring
    floor_distance = smooth_union(floor_distance, hills , 0.3);

    //candy
    vec3 candy_position = vec3( mod(pos.x+ 0.25, 2.), pos.y, mod(pos.z + 0.25, 2.));
    // vec2 id_candy = floor((pos.xz + 0.25) / 0.5);
    // vec2 displacement = 0.1 * cos(vec2(id_candy.x * 72.2 + id_candy.y * 13.7, id_candy.x * 22.2 + id_candy.y * 53.7));
    float candy_dist = sdSphere(candy_position - vec3(1. ,plane_pos_y + 0.03,1.5) , 0.07);
    
    return (floor_distance < candy_dist) ? vec2(floor_distance, floor_id) :  vec2(candy_dist, candy_id) ;
}

vec2 GetDistance(in vec3 pos) // GetDistance : my GetDistance function 
{
    vec2 character_return_vec = sdCharacter(pos);
    float character_distance = character_return_vec.x;
    vec2 landscape_return_vec = sdLandscape(pos);
    float landscape_distance = landscape_return_vec.x;
    return (landscape_distance < character_distance) ? landscape_return_vec : character_return_vec;
}


vec3 GetNormal(in vec3 pos){
    vec3 e = vec3(0.01, 0. ,0.);
    return normalize( vec3(GetDistance(pos + e.xyy).x - GetDistance(pos - e.xyy).x,
                           GetDistance(pos + e.yxy).x - GetDistance(pos - e.yxy).x,
                           GetDistance(pos + e.yyx).x - GetDistance(pos - e.yyx).x )); 
                           // .x to get the distance value, .y to get the id
}


#define max_dist 30.0 

vec2 RayMarch(in vec3 ro, in vec3 rd){  
    float id = -1.0;  
    

    vec2 result = vec2(-1., -1.);

    float t_min = 0.5;
    float max_step = 100.0 ;

    // OPTIMIZATION. Only cast rays up to ymax 
    float ymax = 6.0;
    // float bounding_plane =  (ymax - ro.y)/rd.y; 
    // if (bounding_plane>0) max_step = min(max_step, bounding_plane);

    float t = t_min;

    for (int i = 0; i<250 && i < max_step; i++)
    {
        vec3 pos = ro + t * rd;

        vec2 distance_return_vector = GetDistance(pos);
        float h = distance_return_vector.x;
        id = distance_return_vector.y;
        
        if (abs(h) < 0.0001 * t){
            result = vec2(t, id);
            break;
        }
        
        t += h; // ATTENTION: here we are slowing down the raymarch to avoid 
        
        if (t > max_dist) break;//far clipping plane   
    }
    if (t > max_dist) t = -1;

    return vec2(t, id);
}

float CalculateOcclusion( in vec3 pos, in vec3 normal){
    // float time = osg_FrameTime;
	float occ = 0.0;
    float sca = 1.0;
    for( int i=0; i<5; i++ ){
        float h = 0.01 + 0.11*float(i)/4.0;
        vec3 opos = pos + h*normal;
        float d = GetDistance( opos).x;
        occ += (h-d)*sca;
        sca *= 0.95;
    }
    return clamp( 1.0 - 2.0*occ, 0.0, 1.0 );
}


vec3 GetLight(in vec3 normal, in vec3 pos_of_hit, in vec3 rd){
    vec3 sun_direction    = normalize(vec3(0.8, 0.4, 0.3));
    vec3 sky_direction    = vec3(0.0, 1.0, 0.0);
    vec3 bounce_direction = vec3(0.0, -1.0, 0.0);

    vec3 sun_color        = vec3(7.0, 5.0, 3.0);
    vec3 sky_color        = vec3(0.5, 0.8, 0.95);
    vec3 bounce_color     = vec3(0.75, 0.3, 0.2);
    vec3 fresnel_color    = vec3(1.0, 0.7, 0.5);

    float sun_dif    = clamp(dot(normal, sun_direction), 0.0, 1.0);
    float sky_dif    = clamp(0.6 + 0.5 * dot(normal, sky_direction), 0.0, 1.0);
    float bounce_dif = clamp(0.6 + 0.5 * dot(normal, bounce_direction), 0.0, 1.0);

    float sky_reflection = smoothstep(0.0, 0.5, reflect(rd, normal).y) ;
    float fresnel = clamp(1.0 + dot(rd, normal), 0.0, 1.0);
    float sun_shadow = step( RayMarch(pos_of_hit + normal* 0.01 , sun_direction).x, 0.0) ;

    float occlusion = CalculateOcclusion(pos_of_hit, normal);
    // occlusion *= 2.;
    // return vec3(occlusion );
    return       sun_color * sun_dif * sun_shadow * occlusion +  // primary light from sun
           1.5 * sky_color * sky_dif * occlusion +               //secondary light, ambient light
                 bounce_color * bounce_dif * occlusion  + 
           0.5 * sky_reflection * sky_color * occlusion +
                 fresnel_color * fresnel * (0.3 + 0.7 *sun_dif * occlusion);
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
    vec2 sky_uvs = rd.xz/rd.y;
    float sky_pattern = 1.0 * (sin(1.0*sky_uvs.x) + sin(1.0*sky_uvs.y))+
                        0.5 * (sin(2.0*sky_uvs.x) + sin(2.0*sky_uvs.y));

    float cloud_pattern = smoothstep(0.1, -0.1, 0.5 + sky_pattern); 
    vec3 cloud_color = vec3(0.7,0.8,0.9);
    color = mix(color, cloud_color, cloud_pattern) ; //final background sky color

    vec2 result_vector_of_raymarch = RayMarch(ro, rd);
    float t  = result_vector_of_raymarch.x; // distance
    float id = result_vector_of_raymarch.y; // material

    if (t > 0){ //if we have hit something
        vec3 pos_of_hit = ro + t*rd; 
        vec3 normal = GetNormal(pos_of_hit);

        vec3 object_material = vec3(0.18); // default material albedo

        if (id == floor_id){ //attention when comparing floats
            object_material = vec3(0.05, 0.1 ,0.02); //this material will be textured
            object_material += GetGroundPattern(pos_of_hit)* vec3(0.06, 0.06, 0.02);
        } 
        if (id == skin_id)    { object_material = vec3(0.3,0.12,0.04); }
        if (id == eyes_id)    { object_material = vec3(0.4, 0.4, 0.4); }
        if (id == pupils_id)  { object_material = vec3(0.1, 0.1, 0.4); }
        if (id == candy_id)   { 
            object_material = vec3(0.2, 0.02, 0.01); 
            vec2 id = floor((pos_of_hit.xz + 0.25) / 0.5);
            float f_id = id.x * 11.1 + id.y*32.5;
            object_material += 0.06* cos(f_id*10.0 + vec3(0.0, 0.3, 0.8));
            }

        color = object_material * GetLight(normal, pos_of_hit, rd);
        color = mix( color, vec3(0.5,0.7,0.9), 1.0-exp( -0.00005*t*t*t ) ); //exponential fog
    }   


    //// ------ Color correction
    color = pow( color, vec3(0.4545)); // square root. Gamma correction

    //add contrast
    color = clamp( color , 0.0, 1.0); //make sure color goes from 0 to 1
    vec3 color_with_contrast = color * color * (3. - 2. * color); //cubic function. Increase contrast
    float contrast_blend = 0.7;
    color = contrast_blend * color + (1-contrast_blend) * color_with_contrast;
    
    // color = pow(color, vec3(0.7, 0.9, 1.0)); // fake subsurface scattering, bumping up the reds and oranges in an exponential way, colorizing occlusions (? really? not sure..)
    
    // color = vec3(t/40);
    gl_FragColor = vec4(color , 1.);
}