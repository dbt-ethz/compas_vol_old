#version 120

uniform vec2 u_resolution;
uniform sampler2D color_texture;
uniform sampler2D depth_buffer;
uniform vec3 camera_POS;

uniform mat4 p3d_ProjectionMatrixInverse;
uniform mat4 p3d_ViewMatrixInverse;


vec3 World_position_from_depth(in float depth, in vec2 st){
    st = st * 2.0 - 1.0 ;
    depth =  depth * 2.0 - 1.0;

    vec4 clipSpacePosition =  vec4(st.x, st.y, depth, 1.);

    vec4 viewSpacePosition = p3d_ProjectionMatrixInverse * clipSpacePosition;
    // Perspective division
    // viewSpacePosition *= viewSpacePosition.w;

    vec4 worldSpacePosition = p3d_ViewMatrixInverse * viewSpacePosition;

    return worldSpacePosition.xyz;
    }

void main(){
    vec2 st = gl_FragCoord.xy / u_resolution.xy;
    float aspect_ratio = u_resolution.y / u_resolution.x;

    vec2 texture_uv = st * aspect_ratio;

    vec4 color_pixel = texture2D(color_texture, texture_uv.xy);  
    vec4 depth_pixel = texture2D(depth_buffer, texture_uv .xy); 


    vec3 d = World_position_from_depth(depth_pixel.x, st.xy);



    float dist = length(d - camera_POS);
    
    vec3 color = vec3(1.,1.,1.);
    if (dist > 1000.){
    color = vec3(color_pixel.x, color_pixel.y, color_pixel.z);
    } else {
    color= vec3(1.,1.,0.);
    }

    gl_FragColor = vec4(color,  1.);
    // vec4(color,1.);
}


