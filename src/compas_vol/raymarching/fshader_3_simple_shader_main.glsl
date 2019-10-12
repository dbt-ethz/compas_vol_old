//////// ------------------ Find Ray Direction
uniform mat4 trans_clip_to_model;
uniform mat4 p3d_ViewProjectionMatrixInverse;

vec3 findRayDirection(in vec2 uv, in vec3 ro){
    vec4 pixel_world_coords =  trans_clip_to_model * vec4(uv.x, uv.y, 1., 1.);
    vec3 rd = pixel_world_coords.xyz;
    return normalize(rd);
}


void main(){  
    vec2 st = gl_FragCoord.xy / u_resolution.xy;
    vec2 uv = 2*(st - vec2(0.5, 0.5));
    
    vec3 ro = camera_POS; // ray origin = camera position (world coordinates)
    vec3 rd = findRayDirection(uv, ro);

    float d = RayMarch(ro, rd);
    vec3 p  = ro + rd * d; // position of intersection of ray with solid

    float alpha = 1.0;
    if (d > 200 ){
        alpha = 0.;
    } else {
        alpha = 1.;
    }

    vec3 normal = GetNormal(p);

    vec3 color = normal;
    // color section white
    if (abs(p.y - y_slice) < 0.1) {
        color = vec3(1.);  // so that section becomes white
    }
    gl_FragColor = vec4 (color, alpha);
}





