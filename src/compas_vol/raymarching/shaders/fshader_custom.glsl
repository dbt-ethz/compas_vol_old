#version 120

uniform vec2 u_resolution;
uniform float osg_FrameTime;

float GetDistance(in vec3 pos) // GetDistance : my GetDistance function 
{
    // sphere
    vec3 cen = vec3(0,0.25,0); // sphere x,y,z
    float r = .5; //radius
    float sphere_distance = length(pos - cen) - r; // center, radius 

    // floor 
    float plane_pos_y = -0.25;
    float floor_distance = pos.y - plane_pos_y; 

    return min(sphere_distance, floor_distance);
}


vec3 GetNormal(in vec3 pos){
    vec3 e = vec3(0.01, 0. ,0.);
    return normalize( vec3(GetDistance(pos + e.xyy) - GetDistance(pos - e.xyy),
                           GetDistance(pos + e.yxy) - GetDistance(pos - e.yxy),
                           GetDistance(pos + e.yyx) - GetDistance(pos - e.yyx) ));
}


#define max_dist 30.0 
#define max_step 100.0 
float RayMarch(in vec3 ro, in vec3 rd){    
    float t = 0.0;
    for (int i = 0; i<max_step; i++)
    {
        vec3 pos = ro + t*rd;
        float h = GetDistance(pos);
        if (h < 0.01) break;
        t += h;
        if (t > max_dist) break;//far clipping plane   
    }
    if (t > max_dist) t = -1;
    return t;
}


vec3 GetLight(in vec3 normal, in vec3 pos_of_hit){
    vec3 sun_color = vec3(1.0, 0.8, 0.6);
    vec3 sun_direction = normalize(vec3(0.8, 0.4, 0.3));
    vec3 sky_color = vec3(0.0, 0.07, 0.25);
    vec3 sky_direction  = vec3(0.0, 1.0, 0.0);

    float sun_dif = clamp(dot(normal, sun_direction), 0.0, 1.0);
    float sky_dif = clamp(0.6 + 0.5 * dot(normal, sky_direction), 0.0, 1.0);

    float sun_shadow = step( RayMarch(pos_of_hit + normal* 0.01 , sun_direction), 0.0) ;
    
    return sun_color * sun_dif * sun_shadow + sky_color * sky_dif;
}





void main(){  
    vec2 p = gl_FragCoord.xy / u_resolution.xy;
    p = 2*(p - vec2(0.5, 0.5)); // normalize (put on the center of the screen) 
    
    vec3 ro = vec3(0.0, 1.0, 6.0);
    vec3 rd = normalize(vec3(p.x, p.y, -2.));  //ray direction. Near plane: 1.5 field of view

    vec3 color = vec3(0.0); //background

    float t = RayMarch(ro, rd);

    if (t > 0){
        vec3 pos_of_hit = ro + t*rd; 
        vec3 normal = GetNormal(pos_of_hit);
        color = GetLight(normal, pos_of_hit);
    }

    color = pow( color, vec3(0.4545)); // square root for gamma correction, important!

    gl_FragColor = vec4(color , 1.);

}