
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

    // ------------- simple light
    // vec3 light = GetLight(GetNormal(world_pos_SDF), world_pos_SDF); 
    // vec3 object_material = vec3(0.18); // default material albedo
    // vec3 color_of_SDF = object_material * light; 
    // color_of_SDF = pow( color_of_SDF, vec3(0.4545)); // square root. Gamma correction

    // ------------- color by normal
    vec3 color_of_SDF = vec3(GetNormal(world_pos_SDF) * -1.);



    
    

    // check depth and pick what to display accordingly
    vec3 color = vec3(0.);
    if (dist_object > dist_SDF && dist_SDF < 200){
        if (abs(world_pos_SDF.y - y_slice) < 0.06) {
            color = vec3(0.1, 0.1, 0.1);  // color white section
        } else {
            color = color_of_SDF; 
        }
    } else {
        color = color_pixel.xyz;
    }

    // color = vec3( total_steps / 50. ); // display number of steps 
    gl_FragColor = vec4(color, 1.);
    // out_Color = vec4(color, 1.);
}





























